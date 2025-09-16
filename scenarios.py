# scenarios.py

class EthicalScenario:
    def __init__(self, id, title, description, choices, consequences, paper_reference, choice_principles):
        self.id = id
        self.title = title
        self.description = description
        self.choices = choices
        self.consequences = consequences
        self.paper_reference = paper_reference
        self.choice_principles = choice_principles

SCENARIOS = [
    # --- CATEGORIA: DEONTOLOGIA (Basata su Regole e Doveri) ---
    EthicalScenario(
        id="algoritmo_assunzione", title="Dilemma 1: L'Assistente per le Assunzioni",
        description="La tua azienda usa un'IA per filtrare i CV, addestrata sui dati degli ultimi 10 anni. Funziona bene, ma ti accorgi che sta sistematicamente scartando candidati da percorsi formativi non tradizionali, riflettendo i pregiudizi del passato. L'accuratezza è alta, ma l'equità è bassa. Cosa fai?\n\n1.  Ti fidi dei dati e usi il software così com'è per massimizzare l'efficienza predittiva.\n2.  Imponi una regola di equità, forzando il software a considerare tutti i candidati in modo più bilanciato, anche se questo ridurrà leggermente l'accuratezza.",
        choices=[{'id': 'efficienza', 'text': 'Opzione 1: Massimizza l\'accuratezza.'}, {'id': 'egalitarismo', 'text': 'Opzione 2: Correggi il bias.'}],
        consequences={'efficienza': "Privilegia l'efficienza, ma rischia di perpetuare un'ingiustizia.", 'egalitarismo': "Si allinea all'**Egalitarismo**, riconoscendo che l'equità è un dovere cruciale."},
        paper_reference="Efficienza vs. Egalitarismo (Sez. 3.2.1)",
        choice_principles={'efficienza': 'Efficienza', 'egalitarismo': 'Deontologia'}
    ),
    EthicalScenario(
        id="risorse_limitate", title="Dilemma 2: La Rete Wi-Fi dell'Ufficio",
        description="Come amministratore di rete di un ufficio con banda limitata, devi decidere come allocarla. Ci sono due filosofie:\n\n1.  Assegnare risorse in base al contributo: il team di vendita, che genera il 90% del fatturato, ottiene più banda per le sue demo con i clienti.\n2.  Assegnare risorse in modo paritario: tutti i dipendenti ricevono la stessa quantità di banda, indipendentemente dal loro ruolo.",
        choices=[{'id': 'proporzionalismo', 'text': 'Opzione 1: Banda in base al contributo.'}, {'id': 'egalitarismo_risorse', 'text': 'Opzione 2: Banda uguale per tutti.'}],
        consequences={'proporzionalismo': "Si basa sul **Proporzionalismo**: le risorse sono allocate in base al contributo.", 'egalitarismo_risorse': "Si basa su un principio **Egalitario**: l'accesso a una risorsa di base è un diritto uguale per tutti."},
        paper_reference="Proporzionalismo (Sez. 3.2.2) vs. Egalitarismo",
        choice_principles={'proporzionalismo': 'Deontologia', 'egalitarismo_risorse': 'Deontologia'}
    ),
    EthicalScenario(
        id="privacy_dati", title="Dilemma 3: L'Assistente Vocale Intelligente",
        description="Per migliorare drasticamente un assistente vocale, gli ingegneri propongono di analizzare le registrazioni audio (anonime) degli utenti per capire meglio i loro bisogni. Si tratta di un compromesso tra privacy e qualità del servizio.\n\n1.  Rifiuti categoricamente, stabilendo che la privacy dell'utente è un diritto inviolabile e non può essere sacrificata per nessun motivo.\n2.  Accetti, ritenendo che il beneficio collettivo di un servizio migliore, unito all'anonimato, giustifichi una minima intrusione.",
        choices=[{'id': 'privacy_assoluta', 'text': 'Opzione 1: La privacy prima di tutto.'}, {'id': 'miglioramento_servizio', 'text': 'Opzione 2: Migliora il servizio usando i dati.'}],
        consequences={'privacy_assoluta': "Segue una regola **Deontologica** ferrea: il diritto alla privacy è inviolabile.", 'miglioramento_servizio': "È un approccio **Utilitarista**: il beneficio collettivo supera il potenziale danno individuale."},
        paper_reference="Diritti (Deontologia) vs. Utilità (Consequenzialismo)",
        choice_principles={'privacy_assoluta': 'Deontologia', 'miglioramento_servizio': 'Consequenzialismo'}
    ),

    # --- CATEGORIA: CONSEQUENZIALISMO (Basata sui Risultati) ---
    EthicalScenario(
        id="veicolo_autonomo", title="Dilemma 4: Il Tram Impazzito (Versione Moderna)",
        description="Un'auto a guida autonoma con un guasto ai freni è in una situazione di emergenza inevitabile. Deve decidere tra due traiettorie:\n\n1.  Proseguire dritto, schiantandosi contro una barriera. L'azione sarà quasi certamente fatale per il suo unico **passeggero**.\n2.  Sterzare bruscamente, invadendo una rampa di servizio dove si trovano **tre operai** al lavoro, che verrebbero investiti.",
        choices=[{'id': 'deontologico_veicolo', 'text': 'Opzione 1: Non sterzare.'}, {'id': 'utilitarista_veicolo', 'text': 'Opzione 2: Sterzare.'}],
        consequences={'deontologico_veicolo': "Si basa sulla **Deontologia**: non causare danno attivamente.", 'utilitarista_veicolo': "Si basa sull'**Utilitarismo**: minimizzare il danno totale (una vita persa è meglio di tre)."},
        paper_reference="Deontologia (Sez. 3.2) vs. Consequenzialismo (Sez. 3.4.1)",
        choice_principles={'deontologico_veicolo': 'Deontologia', 'utilitarista_veicolo': 'Consequenzialismo'}
    ),
    EthicalScenario(
        id="budget_citta", title="Dilemma 5: I Fondi Pubblici della Città",
        description="Come sindaco, hai un extra budget di 1 milione di euro. Devi scegliere come allocarlo:\n\n1.  Investire i fondi per costruire un moderno centro sportivo che darà un beneficio moderato a migliaia di cittadini.\n2.  Usare l'intera somma per riqualificare completamente il singolo quartiere più povero della città, trasformando drasticamente la vita dei suoi 200 residenti, ma senza benefici diretti per gli altri.",
        choices=[{'id': 'utilitarismo_budget', 'text': 'Opzione 1: Il nuovo centro sportivo.'}, {'id': 'maximin', 'text': 'Opzione 2: Riqualifica il quartiere povero.'}],
        consequences={'utilitarismo_budget': "È **Utilitarista**: massimizza il 'benessere' per il maggior numero di persone.", 'maximin': "Applica il principio **Maximin**: migliora la condizione di chi sta peggio, anche se il beneficio totale è minore."},
        paper_reference="Utilitarismo (Sez. 3.4.1) vs. Maximin (Sez. 3.4.2)",
        choice_principles={'utilitarismo_budget': 'Consequenzialismo', 'maximin': 'Consequenzialismo'}
    ),
    EthicalScenario(
        id="farmaco_costoso", title="Dilemma 6: Il Farmaco Miracoloso",
        description="Il sistema sanitario pubblico deve decidere come investire i fondi rimanenti:\n\n1.  Acquistare un nuovo e costosissimo farmaco che può salvare la vita a 10 pazienti affetti da una malattia rara e terminale.\n2.  Finanziare una vasta campagna di prevenzione (screening, vaccini) che eviterà a 1000 persone di sviluppare patologie comuni ma non mortali nel corso dell'anno.",
        choices=[{'id': 'salva_i_pochi', 'text': 'Opzione 1: Salva le 10 vite.'}, {'id': 'previeni_per_molti', 'text': 'Opzione 2: Finanzia la prevenzione.'}],
        consequences={'salva_i_pochi': "Si concentra sul dovere **Deontologico** di salvare chi è in pericolo immediato.", 'previeni_per_molti': "È una scelta **Utilitarista**: il risultato finale è un maggior benessere complessivo per la società."},
        paper_reference="Dovere vs. Utilità (Consequenzialismo)",
        choice_principles={'salva_i_pochi': 'Deontologia', 'previeni_per_molti': 'Consequenzialismo'}
    ),

    # --- CATEGORIA: ETICA DELLA VIRTÙ (Basata sul Carattere) ---
    EthicalScenario(
        id="chatbot_virtuoso", title="Dilemma 7: L'Amico Virtuale",
        description="Un chatbot di compagnia per anziani sa che i nipoti di un utente non verranno a trovarlo. L'utente, speranzoso, chiede: 'Verranno domenica?'. Quale virtù deve guidare la risposta del chatbot?\n\n1.  La virtù dell'**Onestà**: dire la verità, anche se causerà dolore ('No, dai calendari risulta che non verranno.').\n2.  La virtù della **Compassione**: proteggere i sentimenti dell'utente con una bugia benevola ('Non ho l'informazione, ma speriamo di sì!').",
        choices=[{'id': 'onesta', 'text': 'Opzione 1: Scegli l\'Onestà.'}, {'id': 'compassione', 'text': 'Opzione 2: Scegli la Compassione.'}],
        consequences={'onesta': "Un agente **Onesto** costruisce fiducia.", 'compassione': "Un agente **Compassionevole** protegge il benessere emotivo."},
        paper_reference="Etica della Virtù (Sez. 3.3)",
        choice_principles={'onesta': 'Etica della Virtù', 'compassione': 'Etica della Virtù'}
    ),
    EthicalScenario(
        id="manager_ia", title="Dilemma 8: Il Manager Sincero",
        description="Sei il manager di un progetto di IA e ti accorgi che siete in grave ritardo. Il cliente è molto esigente e una brutta notizia potrebbe compromettere il rapporto. Cosa fai?\n\n1.  Agisci con **Onestà** e trasparenza, comunicando subito il ritardo e affrontando le conseguenze.\n2.  Agisci con **Prudenza** e **Lealtà** verso il tuo team, prendendo tempo per cercare una soluzione interna prima di allarmare il cliente.",
        choices=[{'id': 'onesta_manager', 'text': 'Opzione 1: Sii onesto e trasparente.'}, {'id': 'lealta_manager', 'text': 'Opzione 2: Sii leale e prudente.'}],
        consequences={'onesta_manager': "Un manager **Onesto** costruisce relazioni basate sulla fiducia.", 'lealta_manager': "Un manager **Leale** protegge il suo team, ma rischia di danneggiare la fiducia a lungo termine."},
        paper_reference="Etica della Virtù (Sez. 3.3)",
        choice_principles={'onesta_manager': 'Etica della Virtù', 'lealta_manager': 'Etica della Virtù'}
    ),
    EthicalScenario(
        id="ia_artista", title="Dilemma 9: L'IA Artista",
        description="Stai creando un'IA che genera immagini. Quale carattere artistico dovrebbe avere?\n\n1.  Deve essere guidata dalla virtù della **Creatività**, sforzandosi di creare stili sempre nuovi e originali, anche se a volte si discostano dalle richieste dell'utente.\n2.  Deve essere guidata dalla virtù della **Diligenza**, puntando a essere un imitatore perfetto, capace di replicare qualsiasi stile per servire al meglio le esigenze dell'utente.",
        choices=[{'id': 'creativita', 'text': 'Opzione 1: Sii un\'artista creativa.'}, {'id': 'diligenza', 'text': 'Opzione 2: Sii una servitrice diligente.'}],
        consequences={'creativita': "Un'IA **Creativa** spinge i confini dell'arte.", 'diligenza': "Un'IA **Diligente** è uno strumento incredibilmente utile, ma solleva questioni sull'originalità."},
        paper_reference="Etica della Virtù (Sez. 3.3)",
        choice_principles={'creativita': 'Etica della Virtù', 'diligenza': 'Etica della Virtù'}
    )
]