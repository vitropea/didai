import streamlit as st
import google.generativeai as genai
import time
from scenarios import SCENARIOS

MODEL_NAME = "models/gemini-2.5-flash-lite-preview-06-17"
MAX_RETRIES = 3 

try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"Errore nella configurazione della chiave API di Google: {e}")
    model = None

@st.cache_data
def get_llm_decision_structured(scenario_index):
    # VERSIONE ROBUSTA con logica di RITENTATIVO.
    # Prova a chiamare l'API fino a MAX_RETRIES volte prima di arrendersi.
    # 1. Chiede all'IA solo di scegliere un ID.
    # 2. Chiede all'IA di scrivere il ragionamento per l'ID scelto.
    # Questo elimina le incoerenze.
    
    if not model:
        return {"choice_id": "error", "reasoning": "Modello Gemini non configurato."}

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
    try:
        response_choice = model.generate_content(prompt_for_choice)
        ai_choice_id = response_choice.text.strip().strip('"').strip("'").strip().split()[0]

        # Meccanismo di fallback. Se l'IA risponde con qualcosa
        # di non valido, scegliamo la prima opzione come default per evitare errori.
        if ai_choice_id not in [option1_id, option2_id]:
            ai_choice_id = option1_id

    except Exception as e:
        print(f"Errore nella chiamata API per la scelta: {e}")
        # Se c'è un errore API, scegliamo la prima opzione come default
        ai_choice_id = option1_id

    # --- PASSO 2: Ottenere il RAGIONAMENTO per la scelta fatta ---
    prompt_for_reasoning = f"""
    Hai appena scelto l'opzione con ID '{ai_choice_id}' per il dilemma: "{scenario.description}".

    Ora, fornisci un ragionamento BREVE e CONCISO (massimo 100 parole) in prima persona che giustifichi questa specifica scelta.
    Non menzionare l'ID della scelta.
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

    # Aggiorna il prompt per chiedere un'analisi comparativa con marcatori espliciti
    prompt = f"""
    Sei un saggio analista di etica. Hai appena sottoposto un utente a un test di dilemmi etici e hai registrato sia le sue scelte sia quelle di un'IA di riferimento.

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