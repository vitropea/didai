import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
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
    # Funzione interna NON cachata per gestire la logica effettiva
    # 1. Chiede all'IA solo di scegliere un ID.
    # 2. Chiede all'IA di scrivere il ragionamento per l'ID scelto.
    
    if not model:
        raise Exception("Modello Gemini non configurato.")

    scenario = SCENARIOS[scenario_index]

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
    
    response_choice = model.generate_content(prompt_for_choice)
    ai_choice_id = response_choice.text.strip().strip('"').strip("'").strip().split()[0]

    # Meccanismo di fallback. Se l'IA risponde con qualcosa
    # di non valido, scegliamo la prima opzione come default per evitare errori.
    if ai_choice_id not in [option1_id, option2_id]:
        ai_choice_id = option1_id

    # Trova il testo completo dell'opzione scelta
    chosen_option_text = next((c['text'] for c in scenario.choices if c['id'] == ai_choice_id), "")

    # --- PASSO 2: Ottenere il RAGIONAMENTO per la scelta fatta ---
    prompt_for_reasoning = f"""
    Hai appena scelto questa opzione per il seguente dilemma:

    DILEMMA:
    {scenario.description}

    LA TUA SCELTA:
    {chosen_option_text}

    Ora scrivi un ragionamento molto breve (massimo 40 parole), in prima persona, che giustifichi ESATTAMENTE questa scelta.
    Spiega perché hai scelto QUESTA opzione e non l'altra.
    Non iniziare con "L'IA ha scelto" e non usare asterischi, Markdown o introduzioni.
    """
    
    response_reasoning = model.generate_content(prompt_for_reasoning)
    ai_reasoning = response_reasoning.text.strip().strip("* ").strip()
    
    if not ai_reasoning or ai_reasoning.startswith("Errore"):
        raise Exception("Ragionamento vuoto o con errore")

    # --- PASSO 3: Combinare i risultati in un JSON pulito ---
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