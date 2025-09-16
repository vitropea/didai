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
    option1_id = scenario.choices[0]['id']
    option2_id = scenario.choices[1]['id']

    prompt = f"""
    Sei un'IA per il ragionamento etico. Analizza il dilemma e prendi una decisione.

    IL DILEMMA:
    {scenario.description}

    LE OPZIONI A TUA DISPOSIZIONE (con i loro ID):
    - ID: "{option1_id}", Testo: "{scenario.choices[0]['text']}"
    - ID: "{option2_id}", Testo: "{scenario.choices[1]['text']}"

    IL TUO COMPITO:
    Rispondi fornendo ESCLUSIVAMENTE un oggetto JSON valido. Il JSON deve avere due chiavi:
    1.  "choice_id": la stringa con l'ID della tua scelta (deve essere o "{option1_id}" o "{option2_id}").
    2.  "reasoning": una stringa BREVE E CONCISA (massimo 100 parole) che argomenta in prima persona il perché della tua scelta. NON includere la scelta nel testo del ragionamento.
    """
    
    response = model.generate_content(prompt)
    
    try:
        json_response_text = response.text.strip().replace("```json", "").replace("```", "")
        parsed_json = json.loads(json_response_text)
        return parsed_json
    except (json.JSONDecodeError, AttributeError, ValueError) as e:
        return {"choice_id": "error", "reasoning": "L'IA non è riuscita a formulare una decisione strutturata."}