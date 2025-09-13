# main.py
import streamlit as st
from llm_gemini import get_llm_response_stream

# --- Configurazione della Pagina ---
st.set_page_config(
    page_title="Dilemmi Etici nell'IA",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Stato della Sessione ---
# Inizializziamo tutti i valori necessari all'inizio
if 'current_scenario_index' not in st.session_state:
    st.session_state.current_scenario_index = 0
if 'choice_made' not in st.session_state:
    st.session_state.choice_made = None

# --- Caricamento Scenari ---
# Importiamo gli scenari solo ora per assicurarci che la configurazione della pagina sia la prima cosa eseguita
from scenarios import SCENARIOS

# --- UI Principale ---
st.title("Laboratorio Interattivo di Etica dell'IA")
st.markdown("Basato sul paper *'Macro Ethics Principles for Responsible AI Systems'*.")
st.markdown("---")

# Controlla se ci sono ancora scenari da mostrare
if st.session_state.current_scenario_index < len(SCENARIOS):
    current_scenario = SCENARIOS[st.session_state.current_scenario_index]

    # Mostra la descrizione dello scenario
    st.header(current_scenario.title)
    st.markdown(current_scenario.description)
    
    st.subheader("Quale decisione prendi?")

    # Gestione delle scelte
    # Se una scelta non è ancora stata fatta per questo scenario, mostra i bottoni
    if st.session_state.choice_made is None:
        col1, col2 = st.columns(2)
        with col1:
            if st.button(current_scenario.choices[0]['text']):
                st.session_state.choice_made = current_scenario.choices[0]['id']
                st.rerun()
        with col2:
            if st.button(current_scenario.choices[1]['text']):
                st.session_state.choice_made = current_scenario.choices[1]['id']
                st.rerun()

    # Se una scelta È stata fatta, mostra l'analisi e il bottone per andare avanti
    if st.session_state.choice_made is not None:
        st.markdown("---")
        
        with st.chat_message("assistant"):
            st.write("Ottima riflessione. Ora analizziamo insieme la tua scelta...")
            stream = get_llm_response_stream(current_scenario, st.session_state.choice_made)
            st.write_stream(stream) 
        
        with st.expander("Mostra l'analisi teorica completa"):
            st.info(f"**Riferimento al paper:** {current_scenario.paper_reference}")
            consequence_text = current_scenario.consequences[st.session_state.choice_made]
            st.markdown(consequence_text)

        st.markdown("---")
        
        # Bottone per passare allo scenario successivo
        if st.button("Prossimo Dilemma"):
            st.session_state.current_scenario_index += 1
            st.session_state.choice_made = None  # Resetta la scelta per il nuovo scenario
            st.rerun()

else:
    # Se l'indice è fuori range, significa che abbiamo finito
    st.success("Hai completato tutti i dilemmi disponibili! Ottimo lavoro.")
    st.balloons()
    if st.button("Ricomincia dall'inizio"):
        # Resetta lo stato per ricominciare
        st.session_state.current_scenario_index = 0
        st.session_state.choice_made = None
        st.rerun()