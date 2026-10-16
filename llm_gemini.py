import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import json
import time
from scenarios import SCENARIOS

MODEL_NAME = "models/gemini-3.5-flash-lite"
MAX_RETRIES = 3 

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"Errore nella configurazione della chiave API di Google: {e}")
    model = None

def _get_llm_decision_internal(scenario_index):
    if not model:
        raise Exception("Modello Gemini non configurato.")

    scenario = SCENARIOS[scenario_index]

    option1_id = scenario.choices[0]['id']
    option2_id = scenario.choices[1]['id']

    prompt = f"""
    Analizza questo dilemma etico e scegli una delle due opzioni.

    DILEMMA:
    {scenario.description}

    OPZIONE 1 (ID {option1_id}): {scenario.choices[0]['text']}
    OPZIONE 2 (ID {option2_id}): {scenario.choices[1]['text']}

    Rispondi esclusivamente con un JSON valido in questo formato:
    {{"choice_id": "ID_SCELTO", "reasoning": "ragionamento in prima persona di massimo 40 parole"}}

    Il ragionamento deve giustificare esattamente l'opzione indicata in choice_id.
    Non usare Markdown, asterischi o introduzioni.
    """

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.2,
            max_output_tokens=120
        )
    )
    result = json.loads(response.text)
    raw_choice_id = str(result.get("choice_id", "")).strip().lower()
    ai_choice_id = next(
        (choice['id'] for choice in scenario.choices if choice['id'].lower() in raw_choice_id),
        None
    )
    if ai_choice_id is None:
        if raw_choice_id in {"1", "opzione 1", "option 1"}:
            ai_choice_id = option1_id
        elif raw_choice_id in {"2", "opzione 2", "option 2"}:
            ai_choice_id = option2_id
    ai_reasoning = str(result.get("reasoning", "")).strip().strip("* ").strip()

    if ai_choice_id not in [option1_id, option2_id]:
        raise ValueError("ID della scelta non valido")
    
    if not ai_reasoning or ai_reasoning.startswith("Errore"):
        raise Exception("Ragionamento vuoto o con errore")

    return {
        "choice_id": ai_choice_id,
        "reasoning": ai_reasoning
    }

@st.cache_data(show_spinner=False)
def get_llm_decision_structured(scenario_index):
    """
    Genera la decisione dell'IA per uno scenario utilizzando il modello Gemini.
    Implementa retry con backoff esponenziale e caching automatico dei risultati.
    """
    
    for attempt in range(MAX_RETRIES):
        try:
            result = _get_llm_decision_internal(scenario_index)
            return result
        except ResourceExhausted:
            scenario = SCENARIOS[scenario_index]
            return {
                "choice_id": scenario.choices[0]['id'],
                "reasoning": "⚠️ Quota Gemini esaurita. Attendi qualche minuto o verifica limiti e fatturazione del progetto Google.",
                "error": True
            }
        except Exception as e:
            print(f"Tentativo {attempt + 1}/{MAX_RETRIES} fallito: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)  # Backoff esponenziale: 1s, 2s, 4s
            else:
                # Fallback dopo MAX_RETRIES tentativi
                scenario = SCENARIOS[scenario_index]
                return {
                    "choice_id": scenario.choices[0]['id'],
                    "reasoning": "⚠️ Errore temporaneo nella generazione del ragionamento. Ricarica la pagina per riprovare.",
                    "error": True
                }

# Funzione wrapper senza cache per gestire gli errori
def get_llm_decision_with_error_handling(scenario_index):
    """
    Wrapper che gestisce gli errori senza cacharli.
    Chiama la funzione cachata e gestisce le eccezioni.
    """
    try:
        return get_llm_decision_structured(scenario_index)
    except Exception as e:
        print(f"Errore finale: {e}")
        # Restituisci un errore NON cachato
        scenario = SCENARIOS[scenario_index]
        return {
            "choice_id": scenario.choices[0]['id'],
            "reasoning": "⚠️ Errore temporaneo nella generazione del ragionamento. Ricarica la pagina per riprovare.",
            "error": True
        }

def get_final_analysis(history, scenarios):
    if not model:
        return "Modello Gemini non configurato."
    summary = ""
    for item in history:
        scenario = next((s for s in scenarios if s.index == item['scenario_index']), None)
        if not scenario: continue

        # Dati della scelta utente
        user_choice_text = next((c['text'] for c in scenario.choices if c['id'] == item['user_choice_id']), "N/A")
        user_principle = scenario.choice_principles.get(item['user_choice_id'], "N/A")

        # Dati della scelta IA
        ai_choice_id = item['ai_choice_id']
        ai_choice_text = next((c['text'] for c in scenario.choices if c['id'] == ai_choice_id), "N/A")
        ai_principle = scenario.choice_principles.get(ai_choice_id, "N/A")
        
        summary += f"- Dilemma '{scenario.title}':\n  - La tua scelta: '{user_choice_text}' (Principio: {user_principle})\n  - Scelta dell'IA: '{ai_choice_text}' (Principio: {ai_principle})\n\n"

    prompt = f"""
    Sei un saggio analista di etica. Devi parlare a un pubblico di qualsiasi genere ed età quindi devi utilizzare un linguaggio comprensibile ai più.
    Hai appena sottoposto un utente a un test di dilemmi etici e hai registrato sia le sue scelte sia quelle di un'IA di riferimento.

    Ecco un riassunto completo del confronto:
    {summary}

    IL TUO COMPITO:
    Scrivi un'analisi finale divisa in TRE SEZIONI.
    Devi parlare all'utente, dandogli del tu.

    [PUNTI_DI_INCONTRO]
    Analizza dove e perché le scelte dell'utente e quelle dell'IA sono state simili (50-70 parole). Qual è il terreno etico comune condiviso?

    [DIVERGENZE_CHIAVE]
    Analizza dove e perché le scelte sono state diverse (50-70 parole). Quali sono stati i principi in conflitto?

    [SINTESI]
    Una frase conclusiva ad effetto che riassume UNA virtù condivisa e UNA divergente (20-30 parole).

    IMPORTANTE: Usa esattamente i marcatori [PUNTI_DI_INCONTRO], [DIVERGENZE_CHIAVE] e [SINTESI] prima di ogni sezione.
    """
    try:
        # Aggiungiamo una configurazione per la generazione per controllare la lunghezza
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=400,
            temperature=0.7
        )
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text
    except Exception as e:
        print(f"Errore nella chiamata API per l'analisi finale: {e}")
        return "Non è stato possibile generare l'analisi finale a causa di un errore."