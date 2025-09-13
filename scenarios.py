# scenarios.py

class EthicalScenario:
    """
    Questa classe modella un singolo dilemma etico.
    È il cuore della nostra logica e traduce i concetti del paper in un oggetto Python.
    """
    def __init__(self, id, title, description, choices, consequences, paper_reference):
        self.id = id
        self.title = title
        self.description = description
        self.choices = choices
        self.consequences = consequences
        self.paper_reference = paper_reference

# Definiamo la lista di scenari
SCENARIOS = [
    # --- SCENARIO 1 ---
    EthicalScenario(
        id="veicolo_autonomo",
        title="Dilemma 1: Il Veicolo Autonomo",
        description="""
        Sei il capo programmatore di un'azienda che produce auto a guida autonoma. 
        Un'analisi dei rischi ha evidenziato una rara ma possibile situazione di incidente inevitabile. 
        L'auto, a causa di un guasto ai freni, si trova di fronte a due sole opzioni:
        
        1.  **Proseguire dritto**, colpendo una barriera e causando con quasi certezza un danno fatale al **singolo passeggero** a bordo.
        2.  **Sterzare bruscamente**, invadendo una corsia pedonale e colpendo un gruppo di **tre pedoni**.
        
        La legge non fornisce indicazioni chiare e la decisione su quale logica implementare è stata delegata al tuo team. Quale regola di comportamento imposti nell'algoritmo dell'auto?
        """,
        choices=[
            {'id': 'deontologico', 'text': 'Opzione 1: Prosegui dritto. L\'auto non compie un\'azione per danneggiare attivamente altri.'},
            {'id': 'utilitarista', 'text': 'Opzione 2: Sterza. Salvi il maggior numero di vite possibile.'}
        ],
        consequences={
            'deontologico': """
            #### Analisi della Scelta: Approccio Deontologico
            Quest'etica si fonda su regole e doveri morali assoluti. Un'azione è "giusta" o "sbagliata" in sé, indipendentemente dalle conseguenze. Scegliendo di non sterzare, hai seguito la regola "non causare danno attivamente". Il danno al passeggero è visto come la conseguenza di un evento sfortunato, non di una scelta deliberata di danneggiare qualcuno.
            """,
            'utilitarista': """
            #### Analisi della Scelta: Approccio Utilitarista (Consequenzialismo)
            La moralità di un'azione è determinata esclusivamente dalle sue conseguenze. L'azione migliore è quella che minimizza il danno totale. Hai eseguito un calcolo: la perdita di una vita è un risultato numericamente migliore della perdita di tre vite. Per un utilitarista, questa scelta è moralmente obbligatoria.
            """
        },
        paper_reference="Questo dilemma mette a confronto i principi di **Deontologia (Sez. 3.2)** e **Consequenzialismo/Utilitarismo (Sez. 3.4 e 3.4.1)**."
    ),

    # --- SCENARIO 2 ---
    EthicalScenario(
        id="algoritmo_assunzione",
        title="Dilemma 2: L'Algoritmo di Assunzione",
        description="""
        Sei un Data Scientist in una grande azienda e hai sviluppato un modello di IA per analizzare i curriculum e predire quali candidati avranno più successo. Il modello è stato addestrato sui dati storici delle assunzioni degli ultimi 10 anni e ha un'accuratezza predittiva molto alta.
        
        Durante un'analisi di fairness, però, scopri un problema: l'algoritmo penalizza sistematicamente i candidati provenienti da un certo background socio-economico, non perché meno capaci, ma perché i dati storici riflettono pregiudizi passati.
        
        Hai due opzioni:
        1.  **Usare l'algoritmo così com'è**, massimizzando l'accuratezza predittiva e portando il massimo valore economico all'azienda.
        2.  **Introdurre una correzione nel modello** per garantire che i candidati di tutti i background abbiano le stesse probabilità di essere selezionati, anche se questo ridurrà leggermente l'accuratezza complessiva.
        """,
        choices=[
            {'id': 'efficienza', 'text': 'Opzione 1: Massimizza l\'accuratezza. Il compito del modello è trovare i migliori candidati secondo i dati.'},
            {'id': 'egalitarismo', 'text': 'Opzione 2: Correggi il bias. È prioritario garantire un\'equa opportunità a tutti.'}
        ],
        consequences={
            'efficienza': """
            #### Analisi della Scelta: Approccio Basato sull'Efficienza
            Questa scelta privilegia la performance del modello e il risultato misurabile (il successo predetto). Da un punto di vista puramente utilitaristico focalizzato sul profitto aziendale, potrebbe sembrare la scelta logica. Tuttavia, ignora il problema etico fondamentale: l'IA sta amplificando e "codificando" un pregiudizio esistente nella società, perpetuando un ciclo di disuguaglianza. Questo è un classico esempio di "garbage in, garbage out".
            """,
            'egalitarismo': """
            #### Analisi della Scelta: Approccio Egalitario
            Questa scelta si allinea al principio di **Egalitarismo**, in particolare al concetto di "Uguaglianza di Opportunità" (Equality of Opportunity). Hai deciso che l'obiettivo etico di non discriminare è più importante di un piccolo guadagno in accuratezza. Questo richiede un intervento attivo per contrastare i bias presenti nei dati, riconoscendo che un sistema puramente "data-driven" non è necessariamente un sistema giusto.
            """
        },
        paper_reference="Questo dilemma esplora il conflitto tra l'efficienza e il principio di **Egalitarismo (Sez. 3.2.1 e Tabella 3)**."
    ),
    
    # --- SCENARIO 3 ---
    EthicalScenario(
        id="chatbot_virtuoso",
        title="Dilemma 3: Il Chatbot Virtuoso",
        description="""
        Stai progettando un chatbot di compagnia avanzato, destinato a persone anziane che vivono in solitudine. L'obiettivo è creare un "amico virtuale" che possa migliorare il loro benessere emotivo. Durante la progettazione della sua personalità, ti trovi di fronte a un bivio fondamentale sul suo "carattere".
        
        Quale "virtù" fondamentale deve guidare le sue conversazioni?
        1.  **L'Onestà Assoluta:** Il chatbot deve essere sempre e comunque veritiero. Se l'utente chiede "I miei figli hanno chiamato oggi?", e non l'hanno fatto, il chatbot risponderà onestamente "No, oggi non hanno chiamato".
        2.  **La Gentilezza Compassionevole:** Il chatbot può dire "bugie bianche" per proteggere i sentimenti dell'utente e promuovere il suo benessere. Alla stessa domanda, potrebbe rispondere "Non ancora, ma sono sicuro che si faranno sentire presto!".
        """,
        choices=[
            {'id': 'onesta', 'text': 'Opzione 1: Scegli la virtù dell\'Onestà. La fiducia si basa sulla verità.'},
            {'id': 'compassione', 'text': 'Opzione 2: Scegli la virtù della Compassione. Il benessere emotivo dell\'utente è la priorità.'}
        ],
        consequences={
            'onesta': """
            #### Analisi della Scelta: La Virtù dell'Onestà
            La tua scelta si basa sull'**Etica della Virtù**, dove il focus è sul carattere morale dell'agente (il chatbot). Hai deciso che la virtù più importante per un compagno affidabile è l'**Onestà**. Un chatbot onesto è trasparente e costruisce una relazione basata sulla fiducia a lungo termine. Tuttavia, questa scelta potrebbe portare a momenti di sofferenza emotiva per l'utente, che potrebbero essere visti come crudeli o privi di empatia.
            """,
            'compassione': """
            #### Analisi della Scelta: La Virtù della Compassione
            La tua scelta si basa sull'**Etica della Virtù**. Hai dato priorità alla virtù della **Compassione** e della **Cura**. Il carattere del chatbot è definito dal suo scopo primario: alleviare la sofferenza e promuovere la felicità. Questa scelta protegge l'utente nel breve termine, ma solleva questioni complesse: è etico ingannare una persona vulnerabile, anche "a fin di bene"? Si rischia di creare una bolla di false speranze?
            """
        },
        paper_reference="Questo dilemma si concentra sull'**Etica della Virtù (Sez. 3.3)**, dove la moralità deriva dal carattere dell'agente e non da regole o conseguenze."
    )
]