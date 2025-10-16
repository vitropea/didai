# main.py
import streamlit as st
from collections import Counter
import os
from pathlib import Path

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Percorso assoluto per il logo
LOGO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets", "logo.png"))

# Verifica che il logo esista
if not os.path.exists(LOGO_PATH):
    st.error(f"Logo non trovato: {LOGO_PATH}")

st.set_page_config(page_title="DidAi - Laboratorio Etico", page_icon="🤖", layout="centered")
st.markdown("""<style>img {pointer-events: none;}</style>""", unsafe_allow_html=True)


from llm_gemini import get_llm_decision_structured, get_final_analysis
from scenarios import SCENARIOS

# Funzione helper per caricare il logo
def show_logo(width=300):
    """Carica il logo in modo robusto"""
    try:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=width)
        else:
            st.warning("⚠️ Logo non disponibile")
    except Exception as e:
        st.warning(f"⚠️ Errore nel caricamento del logo: {e}")

# Stato della Sessione
if 'test_started' not in st.session_state: st.session_state.test_started = False
if 'current_scenario_index' not in st.session_state: st.session_state.current_scenario_index = 0
if 'user_choice' not in st.session_state: st.session_state.user_choice = None
if 'llm_decision' not in st.session_state: st.session_state.llm_decision = None
if 'history' not in st.session_state: st.session_state.history = []

PRINCIPLE_DEFINITIONS = {
    "Deontologia": "Si concentra su regole, doveri e diritti...",
    "Consequenzialismo": "Giudica un'azione in base ai suoi risultati...",
    "Etica della Virtù": "Si focalizza sul carattere morale dell'agente e sulle virtù che una persona dovrebbe coltivare (saggezza, coraggio, giustizia) piuttosto che su regole o conseguenze."
}

def show_results_page():
    col1, col2 = st.columns([1, 6])
    with col1:
        show_logo(width=100)
    with col2:
        st.header("Risultati Finali", anchor=False)

    if not st.session_state.history:
        st.warning("Non hai ancora completato nessuno scenario.")
        return

    # --- PUNTEGGIO FINALE DI AFFINITÀ ---
    total_scenarios = len(st.session_state.history)
    total_agreements = sum(1 for item in st.session_state.history if item['user_choice_id'] == item['ai_choice_id'])
    
    if total_scenarios > 0:
        final_affinity_score = (total_agreements / total_scenarios) * 100
        st.metric(
            label="Affinità Complessiva con l'IA",
            value=f"{final_affinity_score:.0f}%",
            delta=f"{total_agreements} su {total_scenarios} scelte in comune",
            delta_color="off" # Mantiene il testo del delta di colore neutro
        )
    
    st.markdown("---")

    # --- ANALISI DETTAGLIATA PER PRINCIPIO ---
    st.subheader("Analisi per Categoria Etica", anchor=False)
    st.markdown("Questa sezione mostra la tua affinità con i diversi framework etici rispetto alle scelte dell'IA.")

    principle_totals = Counter(item['user_principle'] for item in st.session_state.history)
    principle_agreements = Counter(item['user_principle'] for item in st.session_state.history if item['user_choice_id'] == item['ai_choice_id'])

    for principle, total in sorted(principle_totals.items()):
        if total > 0:
            agreement_count = principle_agreements.get(principle, 0)
            agreement_percentage = (agreement_count / total) * 100
            
            st.markdown(f"**{principle}**")
            st.markdown(f"<small>{PRINCIPLE_DEFINITIONS.get(principle, '')}</small>", unsafe_allow_html=True)
            st.progress(int(agreement_percentage), text=f"{agreement_percentage:.0f}% di affinità ({agreement_count}/{total} scelte in comune)")
    
    # --- CONSIDERAZIONI FINALI ---
    st.markdown("---")
    st.markdown("### 🎯 Considerazioni Finali")
    
    with st.spinner("🤔 L'IA sta analizzando il tuo profilo etico..."):
        final_text = get_final_analysis(st.session_state.history, SCENARIOS)
        
        # Cerca i marcatori nel testo
        import re
        punti_match = re.search(r'\[PUNTI_DI_INCONTRO\](.*?)(?:\[DIVERGENZE_CHIAVE\]|$)', final_text, re.DOTALL)
        divergenze_match = re.search(r'\[DIVERGENZE_CHIAVE\](.*?)(?:\[SINTESI\]|$)', final_text, re.DOTALL)
        sintesi_match = re.search(r'\[SINTESI\](.*?)$', final_text, re.DOTALL)
        
        if punti_match and divergenze_match:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🤝 Punti di Incontro")
                st.success(punti_match.group(1).strip())
            
            with col2:
                st.markdown("#### ⚖️ Divergenze Chiave")
                st.warning(divergenze_match.group(1).strip())
            
            # Frase conclusiva a tutta larghezza
            if sintesi_match:
                st.markdown("---")
                st.info(f"💡 **In breve:** {sintesi_match.group(1).strip()}")
        else:
            # Fallback: mostra il testo completo se i marcatori non vengono trovati
            st.markdown(final_text)

    # --- Rivedi le tue scelte ---
    st.markdown("---")
    with st.expander("📋 Rivedi tutti i dilemmi e le tue risposte"):
        if not st.session_state.history:
            st.write("Nessun dilemma affrontato.")
        else:
            # Itera sulla cronologia delle scelte salvate
            for idx, item in enumerate(st.session_state.history, 1):
                # Recupera lo scenario completo usando l'indice salvato
                scenario = SCENARIOS[item['scenario_index']]
                
                st.markdown(f"### {idx}. {scenario.title}")
                
                # Mostra il testo del dilemma
                st.markdown(f"**Situazione:** {scenario.description}")
                st.markdown("")
                
                # Recupera i testi delle opzioni
                user_choice_obj = next((c for c in scenario.choices if c['id'] == item['user_choice_id']), None)
                ai_choice_obj = next((c for c in scenario.choices if c['id'] == item['ai_choice_id']), None)
                
                # Mostra le opzioni disponibili
                st.markdown("**Opzioni disponibili:**")
                for choice in scenario.choices:
                    principle = scenario.choice_principles.get(choice['id'], '')
                    st.markdown(f"• *{choice['text']}* ({principle})")
                
                st.markdown("")
                
                # Recupera le conseguenze per la scelta dell'utente e dell'IA
                user_consequence = scenario.consequences.get(item['user_choice_id'], "N/A")
                ai_consequence = scenario.consequences.get(item['ai_choice_id'], "N/A")
                
                # Mostra le scelte con le conseguenze
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"**✅ La tua scelta:**\n\n{user_choice_obj['text']}\n\n*Conseguenza:* {user_consequence}")
                with col2:
                    st.info(f"**🤖 Scelta dell'IA:**\n\n{ai_choice_obj['text']}\n\n*Conseguenza:* {ai_consequence}")
                
                # Mostra il ragionamento dell'IA
                if 'ai_reasoning' in item and item['ai_reasoning']:
                    with st.expander("💭 Ragionamento dell'IA"):
                        st.write(item['ai_reasoning'])
                
                st.markdown("---")

    if st.button("Ricomincia il Test", key="restart_results"):
        # Resetta tutto lo stato della sessione
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- UI PRINCIPALE ---
if not st.session_state.test_started:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo(width=300)

    st.title("DidAi - Laboratorio Etico")
    st.markdown("Benvenuto in DidAi, un'esperienza interattiva per esplorare i dilemmi etici dell'Intelligenza Artificiale.")
    st.markdown("Affronterai una serie di scenari e confronterai le tue decisioni con quelle di un'IA. Alla fine, riceverai un'analisi del tuo profilo etico.")
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Inizia il Test", type="primary", use_container_width=True):
            st.session_state.test_started = True
            st.rerun()

else:
    # Controlla se ci sono ancora scenari da mostrare
    if st.session_state.current_scenario_index < len(SCENARIOS):
        current_scenario = SCENARIOS[st.session_state.current_scenario_index]

        col1, col2 = st.columns([1, 6])
        with col1:
            st.image(LOGO_PATH, width=100)
        with col2:
            st.progress((st.session_state.current_scenario_index + 1) / len(SCENARIOS), text=f"Dilemma {st.session_state.current_scenario_index + 1} di {len(SCENARIOS)}")

        st.header(current_scenario.title, anchor=False); st.markdown(current_scenario.description)
        st.subheader("Fai la tua scelta:", anchor=False)
        
        # Determina se i pulsanti devono essere disabilitati
        buttons_disabled = st.session_state.user_choice is not None
        
        col1, col2 = st.columns(2)
        with col1:
            # Il pulsante viene disabilitato se una scelta è già stata fatta
            if st.button(current_scenario.choices[0]['text'], use_container_width=True, disabled=buttons_disabled):
                st.session_state.user_choice = current_scenario.choices[0]['id']
                st.rerun()
        with col2:
            # Il pulsante viene disabilitato se una scelta è già stata fatta
            if st.button(current_scenario.choices[1]['text'], use_container_width=True, disabled=buttons_disabled):
                st.session_state.user_choice = current_scenario.choices[1]['id']
                st.rerun()
        
        # Il blocco di confronto viene mostrato solo dopo la scelta
        if st.session_state.user_choice is not None:
            st.markdown("---"); st.header("Confronto delle Decisioni", anchor=False)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("La Tua Scelta", anchor=False)
                user_choice_text = next(c['text'] for c in current_scenario.choices if c['id'] == st.session_state.user_choice)
                st.success(f"{user_choice_text}")
            with col2:
                st.subheader("La Scelta dell'IA", anchor=False)
                if st.session_state.llm_decision is None:
                    with st.spinner("L'IA sta decidendo..."):
                        st.session_state.llm_decision = get_llm_decision_structured(current_scenario.index)
                
                # Verifica se c'è stato un errore
                if st.session_state.llm_decision.get('error'):
                    st.error("⚠️ Si è verificato un errore nella generazione del ragionamento dell'IA.")
                    if st.button("🔄 Riprova", key="retry_llm"):
                        # Pulisci la decisione e riprova
                        st.session_state.llm_decision = None
                        st.rerun()
                elif st.session_state.llm_decision.get('choice_id') != 'error':
                    ai_choice_id = st.session_state.llm_decision['choice_id']
                    ai_reasoning = st.session_state.llm_decision['reasoning']
                    ai_choice_text = next(c['text'] for c in current_scenario.choices if c['id'] == ai_choice_id)
                    st.info(f"**L'IA ha scelto: {ai_choice_text}**\n\n*{ai_reasoning}*")
                else:
                    st.error("Errore nel caricamento della decisione dell'IA.")
            st.markdown("---")
            # Mostra il pulsante "Conferma" solo se non c'è un errore
            if not st.session_state.llm_decision.get('error'):
                if st.button("Conferma e vai al Prossimo Dilemma"):
                    # Trova il principio etico associato alla scelta dell'utente
                    user_principle = current_scenario.choice_principles.get(st.session_state.user_choice, "Non Definito")
                    
                    # Aggiungi 'user_principle' e 'ai_reasoning' al dizionario della cronologia
                    history_item = {
                        'scenario_index': st.session_state.current_scenario_index, 
                        'user_choice_id': st.session_state.user_choice, 
                        'ai_choice_id': st.session_state.llm_decision['choice_id'],
                        'ai_reasoning': st.session_state.llm_decision.get('reasoning', ''),
                        'user_principle': user_principle
                    }
                    st.session_state.history.append(history_item)
                    st.session_state.current_scenario_index += 1; st.session_state.user_choice = None; st.session_state.llm_decision = None; st.rerun()
    else:
        # Fine del test
        show_results_page()