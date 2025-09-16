# llm_gemini.py
import streamlit as st
import google.generativeai as genai
import json

MODEL_NAME = "models/gemini-1.5-flash-latest"

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"Errore nella configurazione della chiave API di Google: {e}")
    model = None

def get_llm_decision_structured(scenario):
    """
    VERSIONE ROBUSTA A 2 PASSI:
    1. Chiede all'IA solo di scegliere un ID.
    2. Chiede all'IA di scrivere il ragionamento per l'ID scelto.
    Questo elimina le incoerenze.
    """
    if not model:
        return {"choice_id": "error", "reasoning": "Modello Gemini non configurato."}

    option1_id = scenario.choices[0]['id']
    option2_id = scenario.choices[1]['id']

    # --- PASSO 1: Ottenere solo la SCELTA ---
    prompt_for_choice = f"""
    Analizza il seguente dilemma.
    
    DILEMMA:
    {scenario.description}

    OPZIONI (ID): "{option1_id}", "{option2_id}"

    Quale opzione scegli? Rispondi SOLO con l'ID della tua scelta, senza altre parole.
    """
    try:
        response_choice = model.generate_content(prompt_for_choice)
        ai_choice_id = response_choice.text.strip()

        # Safety check: se l'IA risponde con qualcosa di strano, usiamo un default
        if ai_choice_id not in [option1_id, option2_id]:
            print(f"Warning: L'IA ha restituito un ID non valido ('{ai_choice_id}'). Scelta di default: {option1_id}")
            ai_choice_id = option1_id

    except Exception as e:
        print(f"Errore nella chiamata API per la scelta: {e}")
        return {"choice_id": "error", "reasoning": "Errore nel ricevere la scelta dell'IA."}

    # --- PASSO 2: Ottenere il RAGIONAMENTO per la scelta fatta ---
    chosen_option_text = next(c['text'] for c in scenario.choices if c['id'] == ai_choice_id)
    
    prompt_for_reasoning = f"""
    Hai analizzato un dilemma e hai scelto: "{chosen_option_text}".
    
    Ora, fornisci un ragionamento BREVE e CONCISO (massimo 100 parole) in prima persona che giustifichi questa specifica scelta.
    """
    try:
        response_reasoning = model.generate_content(prompt_for_reasoning)
        ai_reasoning = response_reasoning.text.strip()
    except Exception as e:
        print(f"Errore nella chiamata API per il ragionamento: {e}")
        ai_reasoning = "Errore nel generare il ragionamento."

    # --- PASSO 3: Combinare i risultati in un JSON pulito ---
    return {
        "choice_id": ai_choice_id,
        "reasoning": ai_reasoning
    }