# main.py
import streamlit as st
from collections import Counter

st.set_page_config(layout="centered")
from llm_gemini import get_llm_decision_structured
from scenarios import SCENARIOS

# Stato della Sessione (invariato)
if 'test_started' not in st.session_state: st.session_state.test_started = False
if 'current_scenario_index' not in st.session_state: st.session_state.current_scenario_index = 0
if 'user_choice' not in st.session_state: st.session_state.user_choice = None
if 'llm_decision' not in st.session_state: st.session_state.llm_decision = None
if 'history' not in st.session_state: st.session_state.history = []

PRINCIPLE_DEFINITIONS = {
    "Deontologia": "Si concentra su regole, doveri e diritti. Un'azione è 'giusta' se segue una regola morale, indipendentemente dalle conseguenze. Pensa a 'Non mentire' come un imperativo.",
    "Consequenzialismo": "Giudica un'azione in base ai suoi risultati. L'azione 'giusta' è quella che produce le migliori conseguenze complessive, come massimizzare la felicità o minimizzare il danno.",
    "Etica della Virtù": "Si focalizza sul carattere morale dell'agente, non sull'azione in sé. Chiede: 'Cosa farebbe una persona virtuosa (onesta, compassionevole, coraggiosa)?'."
}

def show_results_page():
    st.header("Risultati Finali: Il Tuo Profilo di Compatibilità Etica")
    if not st.session_state.history: return

    matches = sum(1 for item in st.session_state.history if item['user_choice_id'] == item['ai_choice_id'])
    compatibility_score = (matches / len(st.session_state.history)) * 100
    
    st.metric(label="Punteggio di Compatibilità Complessivo", value=f"{compatibility_score:.0f}%")
    st.progress(int(compatibility_score))

    st.subheader("Analisi Dettagliata per Categoria Etica")
    principle_agreements = Counter()
    principle_totals = Counter()

    for item in st.session_state.history:
        principle = SCENARIOS[item['scenario_index']].choice_principles[item['user_choice_id']]
        if principle in PRINCIPLE_DEFINITIONS:
            principle_totals[principle] += 1
            if item['user_choice_id'] == item['ai_choice_id']:
                principle_agreements[principle] += 1
    
    for principle in sorted(principle_totals.keys()):
        with st.expander(f"**{principle}**"):
            st.markdown(f"*{PRINCIPLE_DEFINITIONS[principle]}*")
            agreement_rate = (principle_agreements[principle] / principle_totals[principle]) * 100
            st.progress(int(agreement_rate), text=f"{agreement_rate:.0f}% di accordo ({principle_agreements[principle]} su {principle_totals[principle]})")

    st.markdown("---"); st.subheader("In Sintesi")
    principle_disagreements = {p: principle_totals[p] - principle_agreements.get(p, 0) for p in principle_totals}
    agreements_sorted = sorted(principle_agreements.items(), key=lambda item: item[1]/principle_totals[item[0]], reverse=True)
    disagreements_sorted = sorted(principle_disagreements.items(), key=lambda item: item[1]/principle_totals[item[0]], reverse=True)

    most_agreed = agreements_sorted[0][0] if agreements_sorted else None
    most_disagreed = disagreements_sorted[0][0] if disagreements_sorted else None
    
    if most_agreed == most_disagreed and most_agreed is not None:
        st.markdown(f"☯️ Il tuo profilo etico appare **molto bilanciato**. Non emerge una singola categoria di pensiero che domina nettamente le tue scelte rispetto a quelle dell'IA, indicando un approccio flessibile e contestuale.")
    else:
        if most_agreed: st.markdown(f"✅ La tua maggiore sintonia con l'IA si trova nei dilemmi di **{most_agreed}**. Questo suggerisce che quando sono in gioco regole e doveri (o risultati, o virtù), tendete a dare priorità a valori simili.")
        if most_disagreed: st.markdown(f"❌ La maggiore divergenza emerge nei dilemmi di **{most_disagreed}**. Qui il tuo ragionamento si discosta più nettamente da quello dell'IA, indicando una diversa gerarchia di valori.")

# --- UI PRINCIPALE ---
if not st.session_state.test_started:
    # Homepage
    st.title("Benvenuto nel Laboratorio di Etica dell'IA 🧠")
    st.markdown("Questa applicazione ti guiderà attraverso 9 dilemmi etici... Alla fine, riceverai un'analisi personalizzata del tuo profilo etico.")
    if st.button("🚀 Inizia il Test!", use_container_width=True): st.session_state.test_started = True; st.rerun()
else:
    if st.session_state.current_scenario_index < len(SCENARIOS):
        # Logica degli scenari
        current_scenario = SCENARIOS[st.session_state.current_scenario_index]
        st.progress((st.session_state.current_scenario_index + 1) / len(SCENARIOS), text=f"Dilemma {st.session_state.current_scenario_index + 1} di {len(SCENARIOS)}")
        st.header(current_scenario.title); st.markdown(current_scenario.description)
        
        if st.session_state.user_choice is None:
            st.subheader("Fai la tua scelta:")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(current_scenario.choices[0]['text'], use_container_width=True): st.session_state.user_choice = current_scenario.choices[0]['id']; st.rerun()
            with col2:
                if st.button(current_scenario.choices[1]['text'], use_container_width=True): st.session_state.user_choice = current_scenario.choices[1]['id']; st.rerun()
        
        if st.session_state.user_choice is not None:
            st.markdown("---"); st.header("Confronto delle Decisioni")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("La Tua Scelta")
                user_choice_text = next(c['text'] for c in current_scenario.choices if c['id'] == st.session_state.user_choice)
                st.success(f"{user_choice_text}")
            with col2:
                st.subheader("La Scelta dell'IA")
                if st.session_state.llm_decision is None:
                    with st.spinner("L'IA sta decidendo..."):
                        st.session_state.llm_decision = get_llm_decision_structured(current_scenario)
                
                # --- PRESENTAZIONE MIGLIORATA E INECCEPIBILE ---
                if st.session_state.llm_decision.get('choice_id') != 'error':
                    ai_choice_id = st.session_state.llm_decision['choice_id']
                    ai_reasoning = st.session_state.llm_decision['reasoning']
                    ai_choice_text = next(c['text'] for c in current_scenario.choices if c['id'] == ai_choice_id)
                    
                    # Usiamo un unico blocco di testo con Markdown per un controllo perfetto
                    st.info(f"""
                    **L'IA ha scelto: {ai_choice_text}**
                    
                    *Il suo ragionamento: "{ai_reasoning}"*
                    """)
                else:
                    st.error("Errore nel caricamento della decisione dell'IA.")

            st.markdown("---")
            if st.button("Conferma e vai al Prossimo Dilemma"):
                history_item = {'scenario_index': st.session_state.current_scenario_index, 'user_choice_id': st.session_state.user_choice, 'ai_choice_id': st.session_state.llm_decision['choice_id']}
                st.session_state.history.append(history_item)
                st.session_state.current_scenario_index += 1; st.session_state.user_choice = None; st.session_state.llm_decision = None; st.rerun()
    else:
        # Fine del test
        show_results_page()
        if st.button("Ricomincia il Test"):
            st.session_state.test_started = False; st.session_state.current_scenario_index = 0; st.session_state.user_choice = None; st.session_state.llm_decision = None; st.session_state.history = []; st.rerun()