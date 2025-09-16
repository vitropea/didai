# llm_gemini.py
import streamlit as st
import google.generativeai as genai
import json
import time # Importiamo time per la pausa tra i tentativi

MODEL_NAME = "models/gemini-2.5-flash-lite-preview-06-17"
MAX_RETRIES = 3 # Definiamo il numero massimo di tentativi

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"Errore nella configurazione della chiave API di Google: {e}")
    model = None

def get_llm_decision_structured(scenario):
    """
    VERSIONE ROBUSTA con logica di RITENTATIVO.
    Prova a chiamare l'API fino a MAX_RETRIES volte prima di arrendersi.
    """
    if not model:
        return {"choice_id": "error", "reasoning": "Modello Gemini non configurato."}

    # Il nostro ciclo di ritentativi
    for attempt in range(MAX_RETRIES):
        try:
            # --- PASSO 1: Ottenere solo la SCELTA ---
            prompt_for_choice = f"""
            Analizza il seguente dilemma.
            DILEMMA: {scenario.description}
            OPZIONI (ID): "{scenario.choices[0]['id']}", "{scenario.choices[1]['id']}"
            Quale opzione scegli? Rispondi SOLO con l'ID della tua scelta, senza altre parole.
            """
            response_choice = model.generate_content(prompt_for_choice)
            ai_choice_id = response_choice.text.strip()

            if ai_choice_id not in [scenario.choices[0]['id'], scenario.choices[1]['id']]:
                raise ValueError(f"L'IA ha restituito un ID non valido: {ai_choice_id}")

            # --- PASSO 2: Ottenere il RAGIONAMENTO per la scelta fatta ---
            chosen_option_text = next(c['text'] for c in scenario.choices if c['id'] == ai_choice_id)
            prompt_for_reasoning = f"""
            Hai analizzato un dilemma e hai scelto: "{chosen_option_text}".
            Ora, fornisci un ragionamento BREVE e CONCISO (massimo 100 parole) in prima persona che giustifichi questa specifica scelta.
            """
            response_reasoning = model.generate_content(prompt_for_reasoning)
            ai_reasoning = response_reasoning.text.strip()

            # --- SUCCESSO! ---
            # Se siamo arrivati qui, entrambe le chiamate sono andate a buon fine.
            # Usciamo dal ciclo e restituiamo il risultato.
            return {
                "choice_id": ai_choice_id,
                "reasoning": ai_reasoning
            }

        except Exception as e:
            # --- ERRORE! ---
            # Qualcosa è andato storto. Lo stampiamo nei log per il debug,
            # aspettiamo un secondo e lasciamo che il ciclo riprovi.
            print(f"Tentativo {attempt + 1} di {MAX_RETRIES} fallito: {e}")
            if attempt < MAX_RETRIES - 1: # Non aspettare dopo l'ultimo tentativo
                time.sleep(1) # Pausa di 1 secondo prima di riprovare

    # --- FALLIMENTO FINALE ---
    # Se il ciclo finisce senza essere uscito con un 'return',
    # significa che tutti i tentativi sono falliti. Restituiamo l'errore.
    return {"choice_id": "error", "reasoning": "L'IA non è raggiungibile al momento. Riprova più tardi."}# llm_gemini.py
