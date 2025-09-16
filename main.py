# main.py
import streamlit as st
from collections import Counter

# (Funzione local_css e set_page_config invariate)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.set_page_config(page_title="DidAi - Laboratorio Etico", page_icon="assets/logo.png", layout="centered")
st.markdown("""<style>img {pointer-events: none;}</style>""", unsafe_allow_html=True)


from llm_gemini import get_llm_decision_structured
from scenarios import SCENARIOS

# Stato della Sessione (invariato)
if 'test_started' not in st.session_state: st.session_state.test_started = False
if 'current_scenario_index' not in st.session_state: st.session_state.current_scenario_index = 0
if 'user_choice' not in st.session_state: st.session_state.user_choice = None
if 'llm_decision' not in st.session_state: st.session_state.llm_decision = None
if 'history' not in st.session_state: st.session_state.history = []

PRINCIPLE_DEFINITIONS = {
    "Deontologia": "Si concentra su regole, doveri e diritti...",
    "Consequenzialismo": "Giudica un'azione in base ai suoi risultati...",
    "Etica della Virtù": "Si focalizza sul carattere morale dell'agente..."
}

def show_results_page():
    # --- MODIFICATO: aggiunto anchor=False ---
    st.header("Risultati Finali: Il Tuo Profilo di Compatibilità Etica", anchor=False)
    if not st.session_state.history: return
    
    # (Logica di calcolo invariata)
    matches = sum(1 for item in st.session_state.history if item['user_choice_id'] == item['ai_choice_id'])
    compatibility_score = (matches / len(st.session_state.history)) * 100
    st.metric(label="Punteggio di Compatibilità Complessivo", value=f"{compatibility_score:.0f}%")
    st.progress(int(compatibility_score))

    # --- MODIFICATO: aggiunto anchor=False ---
    st.subheader("Analisi Dettagliata per Categoria Etica", anchor=False)
    # (Logica di analisi invariata)
    principle_agreements = Counter()
    principle_totals = Counter()
    for item in st.session_state.history:
        principle = SCENARIOS[item['scenario_index']].choice_principles.get(item['user_choice_id'], "Altro")
        if principle in PRINCIPLE_DEFINITIONS:
            principle_totals[principle] += 1
            if item['user_choice_id'] == item['ai_choice_id']: principle_agreements[principle] += 1
    for principle in sorted(principle_totals.keys()):
        with st.expander(f"**{principle}**"):
            st.markdown(f"*{PRINCIPLE_DEFINITIONS[principle]}*")
            agreement_rate = (principle_agreements[principle] / principle_totals[principle]) * 100
            st.progress(int(agreement_rate), text=f"{agreement_rate:.0f}% di accordo")

    # --- MODIFICATO: aggiunto anchor=False ---
    st.markdown("---"); st.subheader("In Sintesi", anchor=False)
    # (Logica di feedback invariata)
    principle_disagreements = {p: principle_totals[p] - principle_agreements.get(p, 0) for p in principle_totals}
    agreements_sorted = sorted(principle_agreements.items(), key=lambda item: item[1]/principle_totals[item[0]], reverse=True)
    disagreements_sorted = sorted(principle_disagreements.items(), key=lambda item: item[1]/principle_totals[item[0]], reverse=True)
    most_agreed = agreements_sorted[0][0] if agreements_sorted else None
    most_disagreed = disagreements_sorted[0][0] if disagreements_sorted else None
    if most_agreed == most_disagreed and most_agreed is not None:
        st.markdown(f"☯️ Il tuo profilo etico appare **molto bilanciato**.")
    else:
        if most_agreed: st.markdown(f"✅ La tua maggiore sintonia con l'IA è nei dilemmi di **{most_agreed}**.")
        if most_disagreed: st.markdown(f"❌ La maggiore divergenza emerge nei dilemmi di **{most_disagreed}**.")

# --- UI PRINCIPALE ---
if not st.session_state.test_started:
    # Homepage (invariata)
    _, mid_col, _ = st.columns([1, 2, 1]); 
    with mid_col: st.image("assets/logo.png")
    st.title("Benvenuto nel Laboratorio di Etica dell'IA")
    st.markdown("Questa applicazione ti guiderà attraverso 9 dilemmi etici...")
    if st.button("🚀 Inizia il Test!", use_container_width=True): st.session_state.test_started = True; st.rerun()
else:
    # Logica del test
    _, mid_col, _ = st.columns([2, 1, 2]); 
    with mid_col: st.image("assets/logo.png")
    
    if st.session_state.current_scenario_index < len(SCENARIOS):
        current_scenario = SCENARIOS[st.session_state.current_scenario_index]
        st.progress((st.session_state.current_scenario_index + 1) / len(SCENARIOS), text=f"Dilemma {st.session_state.current_scenario_index + 1} di {len(SCENARIOS)}")
        
        # --- MODIFICATO: aggiunto anchor=False ---
        st.header(current_scenario.title, anchor=False); st.markdown(current_scenario.description)
        
        if st.session_state.user_choice is None:
            # --- MODIFICATO: aggiunto anchor=False ---
            st.subheader("Fai la tua scelta:", anchor=False)
            col1, col2 = st.columns(2)
            with col1:
                if st.button(current_scenario.choices[0]['text'], use_container_width=True): st.session_state.user_choice = current_scenario.choices[0]['id']; st.rerun()
            with col2:
                if st.button(current_scenario.choices[1]['text'], use_container_width=True): st.session_state.user_choice = current_scenario.choices[1]['id']; st.rerun()
        
        if st.session_state.user_choice is not None:
            # --- MODIFICATO: aggiunto anchor=False ---
            st.markdown("---"); st.header("Confronto delle Decisioni", anchor=False)
            col1, col2 = st.columns(2)
            with col1:
                # --- MODIFICATO: aggiunto anchor=False ---
                st.subheader("La Tua Scelta", anchor=False)
                user_choice_text = next(c['text'] for c in current_scenario.choices if c['id'] == st.session_state.user_choice)
                st.success(f"{user_choice_text}")
            with col2:
                # --- MODIFICATO: aggiunto anchor=False ---
                st.subheader("La Scelta dell'IA", anchor=False)
                if st.session_state.llm_decision is None:
                    with st.spinner("L'IA sta decidendo..."):
                        st.session_state.llm_decision = get_llm_decision_structured(current_scenario)
                if st.session_state.llm_decision.get('choice_id') != 'error':
                    ai_choice_id = st.session_state.llm_decision['choice_id']
                    ai_reasoning = st.session_state.llm_decision['reasoning']
                    ai_choice_text = next(c['text'] for c in current_scenario.choices if c['id'] == ai_choice_id)
                    st.info(f"**L'IA ha scelto: {ai_choice_text}**\n\n*Il suo ragionamento: \"{ai_reasoning}\"*")
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