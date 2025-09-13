# llm_gemini.py
import streamlit as st
import google.generativeai as genai
import time

MODEL_NAME = "gemini-1.5-flash-latest"

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"Errore nella configurazione della chiave API di Google: {e}")
    model = None

def get_socratic_prompt(scenario, user_choice_id):
    """
    Questa funzione è identica a prima, genera il prompt per l'LLM.
    La logica del prompt non dipende dal modello, quindi possiamo riciclarla.
    """
    user_choice_text = next(c['text'] for c in scenario.choices if c['id'] == user_choice_id)
    ethical_principle = "Deontologia" if user_choice_id == 'deontologico' else "Utilitarismo"
    
    prompt = f"""
    Sei un assistente didattico esperto di etica dell'IA, specializzato nel metodo socratico.
    Uno studente sta affrontando un dilemma etico e ha appena fatto una scelta. Il tuo compito è aiutarlo a riflettere, non dargli la risposta.

    IL DILEMMA:
    {scenario.description}

    LA SCELTA DELLO STUDENTE:
    "{user_choice_text}"

    IL TUO COMPITO:
    1.  Rivolgiti allo studente in modo incoraggiante.
    2.  Fagli una o due domande aperte e mirate che lo spingano a giustificare il *perché* della sua scelta. Le domande devono aiutarlo a verbalizzare il ragionamento sottostante.
    3.  Guida la sua riflessione verso il concetto di "{ethical_principle}", ma NON nominare ancora questo termine.
    4.  Sii conciso e mantieni un tono colloquiale e accademico.
    """
    return prompt

def get_llm_response_stream(scenario, user_choice_id):
    """
    Interroga il modello Gemini e restituisce uno stream della risposta.
    """
    if not model:
        # Usiamo un generatore per restituire l'errore in modo che st.write_stream possa gestirlo
        yield "Modello Gemini non configurato. Controlla la tua API key."
        return

    prompt = get_socratic_prompt(scenario, user_choice_id)
    
    # API call per Gemini con streaming
    response_stream = model.generate_content(prompt, stream=True)
    
    for chunk in response_stream:
        # Piccolo ritardo per rendere lo streaming più fluido e visibile
        time.sleep(0.05) 
        yield chunk.text