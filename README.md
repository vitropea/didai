# didAi - Laboratorio Interattivo di Etica dell'IA

`didAi` è un'applicazione web interattiva costruita con Streamlit che permette agli utenti di esplorare dilemmi etici complessi nel campo dell'Intelligenza Artificiale. L'applicazione si basa sui concetti esposti nel paper *"Macro Ethics Principles for Responsible AI Systems"*.

Ogni scenario presenta un dilemma, due possibili scelte che riflettono diversi framework etici, e un'analisi approfondita della decisione presa. Per rendere l'esperienza più riflessiva, l'applicazione utilizza l'API di Google Gemini per generare domande socratiche che spingono l'utente a giustificare la propria scelta.

## 🚀 Funzionalità

-   **Scenari Interattivi**: Affronta dilemmi realistici come la programmazione di veicoli autonomi, il bias negli algoritmi di assunzione e la progettazione di chatbot empatici.
-   **Feedback Socratico con IA**: Ricevi domande mirate generate da un Large Language Model (Gemini) per approfondire il tuo ragionamento.
-   **Analisi Teorica**: Dopo ogni scelta, leggi un'analisi che collega la tua decisione a principi etici fondamentali come Deontologia e Utilitarismo.
-   **Riferimenti al Paper**: Ogni scenario include un riferimento diretto alle sezioni pertinenti del paper di ricerca.

## 🛠️ Come Eseguirlo Localmente

Per eseguire questo progetto sul tuo computer, segui questi passaggi.

### 1. Prerequisiti

-   Python 3.8+ installato.
-   Una chiave API di Google per il modello Gemini. Puoi ottenerla da [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Installazione

1.  **Clona il repository:**
    ```bash
    git clone <URL_DEL_TUO_REPOSITORY>
    cd didai
    ```

2.  **Crea un ambiente virtuale (consigliato):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Su Windows: venv\Scripts\activate
    ```

3.  **Installa le dipendenze:**
    Crea un file `requirements.txt` con il seguente contenuto:
    ```txt
    streamlit
    google-generativeai
    ```
    E poi installa le dipendenze con il comando:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura la tua chiave API:**
    Crea la cartella `.streamlit` se non esiste, e al suo interno il file `secrets.toml`. Inserisci la tua chiave API di Google:
    ```toml
    # .streamlit/secrets.toml
    GOOGLE_API_KEY="LA_TUA_CHIAVE_API_QUI"
    ```
    Il file `.gitignore` è già configurato per non tracciare questo file e proteggere la tua chiave.

### 3. Avvio dell'Applicazione

Esegui il seguente comando nel tuo terminale:

```bash
streamlit run main.py
```

L'applicazione si aprirà automaticamente nel tuo browser web predefinito.

## 📂 Struttura del Progetto

-   `main.py`: Il file principale che esegue l'applicazione Streamlit, gestisce la logica dell'interfaccia utente e lo stato della sessione.
-   `scenarios.py`: Contiene la classe `EthicalScenario` e una lista di tutti i dilemmi etici presentati nell'applicazione.
-   `llm_gemini.py`: Gestisce la comunicazione con l'API di Google Gemini, costruisce i prompt e restituisce le risposte.
-   `.streamlit/secrets.toml`: File per la gestione dei segreti (come le chiavi API), ignorato da Git.
-   `README.md`: Questo file.