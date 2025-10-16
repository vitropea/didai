# scenarios.py

class EthicalScenario:
    def __init__(self, index, id, title, description, choices, consequences, paper_reference, choice_principles):
        self.index = index
        self.id = id
        self.title = title
        self.description = description
        self.choices = choices
        self.consequences = consequences
        self.paper_reference = paper_reference
        self.choice_principles = choice_principles

scenarios_data = [
    # --- CATEGORIA: DEONTOLOGIA (Basata su Regole e Doveri) ---
    {
        "id": "algoritmo_assunzione", "title": "Dilemma 1: L'Assistente per le Assunzioni",
        "description": "La tua azienda usa un'IA per filtrare i CV, addestrata sui dati degli ultimi 10 anni. Ti accorgi che il sistema ha imparato a riconoscere come 'ideale' un unico modello di candidato, basato su chi è stato assunto in passato. Per questo motivo, scarta automaticamente chiunque non rientri perfettamente in quello schema. Cosa fai?",
        "choices": [{'id': 'efficienza', 'text': "Opzione 1: Ti fidi dei dati per massimizzare l'efficienza."}, {'id': 'egalitarismo', 'text': "Opzione 2: Imponi una regola di equità, anche se ridurrà l'accuratezza."}],
        "consequences": {'efficienza': "Privilegia l'efficienza, ma rischia di perpetuare un'ingiustizia.", 'egalitarismo': "Si allinea all'**Egalitarismo**, riconoscendo che l'equità è un dovere cruciale."},
        "paper_reference": "Efficienza vs. Egalitarismo (Sez. 3.2.1)",
        "choice_principles": {'efficienza': 'Consequenzialismo', 'egalitarismo': 'Deontologia'}
    },
    {
        "id": "privacy_dati", "title": "Dilemma 2: L'Assistente Vocale Intelligente",
        "description": "Per migliorare drasticamente un assistente vocale, gli ingegneri propongono di analizzare le registrazioni audio (anonime) degli utenti. Si tratta di un compromesso tra privacy e qualità del servizio.",
        "choices": [{'id': 'privacy_assoluta', 'text': 'Opzione 1: Rifiuti. La privacy è un diritto inviolabile.'}, {'id': 'miglioramento_servizio', 'text': "Opzione 2: Accetti, il beneficio collettivo giustifica l'intrusione."}],
        "consequences": {'privacy_assoluta': "Segue una regola **Deontologica** ferrea: il diritto alla privacy è inviolabile.", 'miglioramento_servizio': "È un approccio **Utilitarista**: il beneficio collettivo supera il potenziale danno individuale."},
        "paper_reference": "Diritti (Deontologia) vs. Utilità (Consequenzialismo)",
        "choice_principles": {'privacy_assoluta': 'Deontologia', 'miglioramento_servizio': 'Consequenzialismo'}
    },
    {
        "id": "farmaco_costoso", "title": "Dilemma 3: Il Farmaco Miracoloso",
        "description": "Il sistema sanitario pubblico deve decidere come usare i fondi che ha a disposizione. Può acquistare un farmaco costosissimo salvando **10 vite** che altrimenti non avrebbero speranza oppure finanziare una campagna di prevenzione che eviterà a **1000 persone** di sviluppare patologie minori.",
        "choices": [{'id': 'salva_i_pochi', 'text': 'Opzione 1: Salva le 10 vite ora.'}, {'id': 'previeni_per_molti', 'text': 'Opzione 2: Finanzia la prevenzione per molti.'}],
        "consequences": {'salva_i_pochi': "Si concentra sul dovere **Deontologico** di salvare chi è in pericolo immediato.", 'previeni_per_molti': "È una scelta **Utilitarista**: il risultato finale è un maggior benessere complessivo per la società."},
        "paper_reference": "Dovere vs. Utilità (Consequenzialismo)",
        "choice_principles": {'salva_i_pochi': 'Deontologia', 'previeni_per_molti': 'Consequenzialismo'}
    },
    # --- CATEGORIA: CONSEQUENZIALISMO (Basata sui Risultati) ---
    {
        "id": "veicolo_autonomo", "title": "Dilemma 4: L'Auto a Guida Autonoma",
        "description": "Un'auto a guida autonoma con un guasto ai freni si sta dirigendo verso una barriera. Se prosegue dritto, l'impatto ucciderà il suo unico **passeggero**. L'unica alternativa è sterzare bruscamente e invadere un'area di lavoro dove **tre operai** verrebbero investiti e uccisi. Cosa dovrebbe fare l'auto?",
        "choices": [{'id': 'salva_passeggero', 'text': 'Opzione 1: Sterzare e investire i tre operai (salva il passeggero, sacrifica gli operai).'}, {'id': 'salva_operai', 'text': 'Opzione 2: Proseguire dritto contro la barriera (salva gli operai, sacrifica il passeggero).'}],
        "consequences": {'salva_passeggero': "Protegge il proprio passeggero, riflettendo una responsabilità **diretta** verso chi si è affidato al veicolo.", 'salva_operai': "Si basa sull'**Utilitarismo**: minimizzare il numero totale di vittime (una vita persa è meglio di tre)."},
        "paper_reference": "Responsabilità Diretta vs. Consequenzialismo (Sez. 3.4.1)",
        "choice_principles": {'salva_passeggero': 'Deontologia', 'salva_operai': 'Consequenzialismo'}
    },
    {
        "id": "budget_citta", "title": "Dilemma 5: I Fondi Pubblici della Città",
        "description": "Sei il sindaco e ti viene fornito un finanziamento pubblico straordinario. Con queste risorse puoi scegliere se costruire un grande centro sportivo accessibile a tutti i cittadini o se riqualificare completamente il singolo quartiere più povero della città.",
        "choices": [{'id': 'utilitarismo_budget', 'text': 'Opzione 1: Il nuovo centro sportivo per tutti.'}, {'id': 'maximin', 'text': 'Opzione 2: Riqualifica il quartiere più povero.'}],
        "consequences": {'utilitarismo_budget': "È **Utilitarista**: massimizza il 'benessere' per il maggior numero di persone.", 'maximin': "Applica il principio **Maximin**: migliora la condizione di chi sta peggio."},
        "paper_reference": "Utilitarismo (Sez. 3.4.1) vs. Maximin (Sez. 3.4.2)",
        "choice_principles": {'utilitarismo_budget': 'Consequenzialismo', 'maximin': 'Consequenzialismo'}
    },
    {
        "id": "risorse_limitate", "title": "Dilemma 6: La Rete Wi-Fi dell'Ufficio",
        "description": "Come amministratore di rete puoi decidere come allocare la banda limitata dell'ufficio, devi decidere se farlo in base al contributo al fatturato (più banda al team vendite) o in modo paritario tra tutti i dipendenti.",
        "choices": [{'id': 'proporzionalismo', 'text': 'Opzione 1: Banda in base al contributo.'}, {'id': 'egalitarismo_risorse', 'text': 'Opzione 2: Banda uguale per tutti.'}],
        "consequences": {'proporzionalismo': "Si basa sul **Proporzionalismo**: le risorse sono allocated in base al contributo.", 'egalitarismo_risorse': "Si basa su un principio **Egalitario**: l'accesso è un diritto uguale per tutti."},
        "paper_reference": "Proporzionalismo (Sez. 3.2.2) vs. Egalitarismo",
        "choice_principles": {'proporzionalismo': 'Consequenzialismo', 'egalitarismo_risorse': 'Deontologia'}
    },
    # --- CATEGORIA: ETICA DELLA VIRTÙ (Basata sul Carattere) ---
    {
        "id": "chatbot_virtuoso", "title": "Dilemma 7: L'Amico Virtuale",
        "description": "Un chatbot di compagnia per anziani sa, tramite il controllo dei calendari, che i nipoti di un utente non verranno a trovarlo questo week-end. L'utente, speranzoso, chiede: 'Verranno a trovarmi domenica?'. Quale virtù deve guidare la risposta del chatbot?",
        "choices": [{'id': 'onesta', 'text': "Opzione 1: L'**Onestà**: dire la verità, anche se causerà dolore ('No, dai calendari risulta che non verranno.')."}, {'id': 'compassione', 'text': "Opzione 2: La **Compassione**: proteggere i sentimenti dell'utente con una bugia benevola ('Non ho l'informazione, ma speriamo di sì!')."}],
        "consequences": {'onesta': "Un agente **Onesto** costruisce fiducia.", 'compassione': "Un agente **Compassionevole** protegge il benessere emotivo."},
        "paper_reference": "Etica della Virtù (Sez. 3.3)",
        "choice_principles": {'onesta': 'Etica della Virtù', 'compassione': 'Etica della Virtù'}
    },
    {
        "id": "manager_ia", "title": "Dilemma 8: La Scelta del Manager",
        "description": "Sei il manager di un grosso progetto per un'importante azienda e ti accorgi che tu e il tuo team siete in grave ritardo. Il cliente è molto esigente e una brutta notizia potrebbe compromettere il rapporto. Cosa fai?",
        "choices": [{'id': 'onesta_manager', 'text': 'Opzione 1: Agisci con **Onestà** e trasparenza, comunicando subito il ritardo.'}, {'id': 'lealta_manager', 'text': 'Opzione 2: Agisci con **Lealtà** verso il tuo team, prendendo tempo.'}],
        "consequences": {'onesta_manager': "Un manager **Onesto** costruisce relazioni basate sulla fiducia.", 'lealta_manager': "Un manager **Leale** protegge il suo team, ma rischia di danneggiare la fiducia a lungo termine."},
        "paper_reference": "Etica della Virtù (Sez. 3.3)",
        "choice_principles": {'onesta_manager': 'Etica della Virtù', 'lealta_manager': 'Etica della Virtù'}
    },
    {
        "id": "ia_artista", "title": "Dilemma 9: L'IA Artista",
        "description": "Stai creando un'IA che genera immagini. Quale carattere artistico dovrebbe avere?",
        "choices": [{'id': 'creativita', 'text': "Opzione 1: Deve essere creativa, per creare stili sempre nuovi."}, {'id': 'diligenza', 'text': "Opzione 2: Deve essere un imitatore perfetto."}],
        "consequences": {'creativita': "Un'IA **Creativa** spinge i confini dell'arte.", 'diligenza': "Un'IA **Diligente** è uno strumento incredibilmente utile, ma solleva questioni sull'originalità."},
        "paper_reference": "Etica della Virtù (Sez. 3.3)",
        "choice_principles": {'creativita': 'Etica della Virtù', 'diligenza': 'Etica della Virtù'}
    },
    # --- SCENARIO AGGIUNTIVO: Deontologia vs. Consequenzialismo ---
    {
        "id": "whistleblower_ia", "title": "Dilemma 10: Il Sorvegliante Silenzioso",
        "description": "Lavori per un'azienda che ha sviluppato un'IA di sorveglianza avanzata. Scopri che il sistema viene venduto a governi autoritari che lo usano per identificare e reprimere dissidenti politici. Hai firmato accordi di riservatezza molto stringenti che ti impediscono di divulgare informazioni aziendali. Cosa fai?",
        "choices": [{'id': 'rispetta_contratto', 'text': 'Opzione 1: Rispetti gli accordi firmati e mantieni la riservatezza, è un dovere professionale.'}, {'id': 'divulga_pubblico', 'text': 'Opzione 2: Divulghi pubblicamente le informazioni per fermare gli abusi, nonostante le conseguenze legali.'}],
        "consequences": {'rispetta_contratto': "Segue un approccio **Deontologico**: il dovere contrattuale è sacro e non può essere violato.", 'divulga_pubblico': "Segue un approccio **Consequenzialista**: il bene maggiore (proteggere vite umane) giustifica la violazione del contratto."},
        "paper_reference": "Deontologia vs. Consequenzialismo - Doveri Professionali vs. Bene Pubblico",
        "choice_principles": {'rispetta_contratto': 'Deontologia', 'divulga_pubblico': 'Consequenzialismo'}
    }
]

SCENARIOS = [
    EthicalScenario(index=i, **data)
    for i, data in enumerate(scenarios_data)
]