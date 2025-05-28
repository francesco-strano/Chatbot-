from db_utils import execute_query

# Dati di esempio per la tabella Strumenti
strumenti_data = [
    ("EnCase", "Software per l'analisi forense di dischi rigidi."),
    ("FTK", "Toolkit forense per l'analisi di dispositivi digitali."),
    ("Wireshark", "Strumento per l'analisi del traffico di rete."),
    ("Autopsy", "Software open source per l'analisi forense di file."),
    ("XRY", "Strumento per l'estrazione e l'analisi di dati da dispositivi mobili."),
    ("Volatility", "Framework per l'analisi forense della memoria."),
    ("Oxygen Forensic Suite", "Software per l'analisi di dispositivi mobili."),
    ("Cellebrite UFED", "Strumento per l'estrazione e l'analisi di dati mobili."),
    ("Nmap", "Strumento per la scansione delle reti e l'analisi di vulnerabilità."),
    ("TCPdump", "Strumento per catturare pacchetti di rete."),
    ("Hashcat", "Strumento per il cracking di password."),
    ("John the Ripper", "Software per il recupero di password."),
    ("ProDiscover", "Strumento per la gestione e l'analisi di dati forensi."),
    ("Belkasoft Evidence Center", "Toolkit per l'analisi forense di dati digitali."),
    ("Recuva", "Software per il recupero di file cancellati."),
    ("PC-3000", "Strumento hardware per la riparazione e il recupero di dati."),
    ("SQLmap", "Strumento per il test di vulnerabilità SQL Injection."),
    ("Burp Suite", "Software per il test di sicurezza delle applicazioni web."),
    ("IDA Pro", "Strumento per l'analisi e il debug di binari."),
    ("Radare2", "Framework open source per l'analisi di binari."),
    ("Kali Linux", "Sistema operativo con strumenti di analisi forense e pen testing."),
    ("Parrot Security OS", "Sistema operativo orientato alla sicurezza informatica."),
    ("Cyber Triage", "Strumento per l'analisi forense live."),
    ("Aircrack-ng", "Strumento per l'analisi e il cracking di reti Wi-Fi."),
    ("Maltego", "Strumento per la raccolta e l'analisi di informazioni OSINT."),
    ("Binwalk", "Strumento per l'analisi di file binari."),
    ("ExifTool", "Strumento per l'analisi dei metadati di file."),
    ("TestDisk", "Strumento per il recupero di partizioni perse."),
    ("Foremost", "Strumento per il recupero di file cancellati."),
    ("Hiew", "Editor binario per l'analisi di file eseguibili.")
]

# Dati di esempio per la tabella Procedure
procedure_data = [
    ("Analisi di disco", "Processo per analizzare un disco rigido per dati cancellati."),
    ("Analisi di rete", "Processo per analizzare i pacchetti di rete per tracce digitali."),
    ("Recupero file cancellati", "Procedure per ripristinare file eliminati."),
    ("Analisi di metadati", "Studio dei metadati dei file per tracciare modifiche e autori."),
    ("Analisi della RAM", "Processo per estrarre dati volatili dalla memoria."),
    ("Carving dei file", "Tecnica per recuperare frammenti di file danneggiati."),
    ("Analisi delle immagini", "Procedure per rilevare alterazioni e tracce nei file immagine."),
    ("Recupero di messaggi", "Estrazione di SMS, chat e messaggi cancellati."),
    ("Identificazione malware", "Procedura per identificare e isolare software dannosi."),
    ("Reverse engineering", "Analisi del funzionamento di software binari."),
    ("Analisi temporale", "Ricostruzione di timeline per incidenti informatici."),
    ("Documentazione delle prove", "Registrazione di ogni attività svolta durante le analisi."),
    ("Raccolta delle prove", "Estrazione sicura e conservazione di dati sensibili."),
    ("Verifica dell'integrità", "Calcolo di hash per garantire l'integrità dei dati."),
    ("Analisi OSINT", "Raccolta di informazioni disponibili pubblicamente."),
    ("Analisi di dispositivi mobili", "Estrazione e analisi di dati da smartphone."),
    ("Valutazione dei log", "Analisi dei file di log per tracciare attività."),
    ("Analisi di rete Wi-Fi", "Valutazione di attività sospette su reti senza fili."),
    ("Recupero da RAID", "Tecniche per recuperare dati da array RAID corrotti."),
    ("Analisi avanzata di malware", "Tecniche per dissezionare software dannosi complessi."),
    ("Recupero da SSD", "Procedure per estrarre dati da SSD danneggiati."),
    ("Analisi di phishing", "Identificazione di attacchi di phishing tramite email."),
    ("Analisi delle email", "Studio dei metadati e dei contenuti delle email."),
    ("Verifica dell'autenticità di documenti", "Conferma dell'autenticità di documenti digitali."),
    ("Analisi di exploit", "Valutazione di vulnerabilità sfruttate."),
    ("Raccolta di chat vocali", "Estrazione di registrazioni audio e vocali."),
    ("Raccolta dati cloud", "Tecniche per estrarre dati da piattaforme cloud."),
    ("Analisi blockchain", "Tracciamento di transazioni su blockchain."),
    ("Documentazione fotografica", "Uso di foto per documentare scene del crimine."),
    ("Crittanalisi", "Decifratura di dati crittografati.")
]

# Dati di esempio per la tabella Normativa
normativa_data = [
    ("GDPR", "Regolamento generale sulla protezione dei dati."),
    ("ISO/IEC 27001", "Standard internazionale per la gestione della sicurezza delle informazioni."),
    ("HIPAA", "Legge statunitense sulla protezione delle informazioni sanitarie."),
    ("NIST 800-53", "Linee guida di sicurezza per i sistemi informatici federali."),
    ("PCI DSS", "Standard di sicurezza per i dati delle carte di pagamento."),
    ("CCPA", "Legge sulla protezione dei dati personali in California."),
    ("LGPD", "Legge generale sulla protezione dei dati in Brasile."),
    ("ISO/IEC 27017", "Standard per la sicurezza del cloud computing."),
    ("FERPA", "Legge statunitense sulla protezione delle informazioni educative."),
    ("Data Protection Act", "Legge sulla protezione dei dati nel Regno Unito."),
    ("FISMA", "Legge federale statunitense sulla sicurezza dei sistemi IT."),
    ("Cybersecurity Act", "Regolamento europeo sulla sicurezza informatica."),
    ("SOX", "Legge statunitense sulla trasparenza delle informazioni finanziarie."),
    ("Basel III", "Normative per il settore bancario internazionale."),
    ("DORA", "Regolamento europeo sulla resilienza operativa digitale."),
    ("MiFID II", "Direttiva europea sui mercati finanziari."),
    ("PSD2", "Direttiva europea sui pagamenti elettronici."),
    ("ePrivacy Regulation", "Normativa europea sulla privacy nelle comunicazioni elettroniche."),
    ("Safe Harbor", "Accordo (ora obsoleto) per la protezione dei dati UE-USA."),
    ("Privacy Shield", "Successore di Safe Harbor per la protezione dei dati UE-USA."),
    ("Schrems II", "Decisione UE sulla protezione dei dati personali trasferiti negli USA."),
    ("E-SIGN Act", "Legge statunitense sulle firme elettroniche."),
    ("Cybersecurity Law", "Legge cinese sulla sicurezza informatica."),
    ("Australian Privacy Act", "Legge sulla protezione dei dati in Australia."),
    ("IT Act", "Legge sull'Information Technology in India."),
    ("Convention 108+", "Trattato internazionale sulla protezione dei dati."),
    ("Directive 95/46/EC", "Direttiva europea sulla protezione dei dati personali."),
    ("Loi Informatique et Libertés", "Legge francese sulla protezione dei dati."),
    ("Singapore PDPA", "Legge sulla protezione dei dati personali a Singapore."),
    ("New Zealand Privacy Act", "Legge sulla protezione dei dati in Nuova Zelanda."),
]

# Dati di esempio per la tabella Casi
casi_data = [
    ("Caso di hacking aziendale", "Violazione dei sistemi IT di una grande azienda."),
    ("Caso di phishing", "Furto di credenziali tramite email fraudolente."),
    ("Caso di furto di identità", "Uso illecito delle informazioni personali di una vittima."),
    ("Caso di insider trading", "Uso di informazioni riservate per speculazioni di borsa."),
    ("Caso di malware bancario", "Infezione di un sistema con malware per sottrarre fondi."),
    ("Caso di ransomware", "Sistema bloccato da un malware che richiede un riscatto."),
    ("Caso di revenge porn", "Pubblicazione non consensuale di materiale privato."),
    ("Caso di cyberbullismo", "Uso di piattaforme digitali per molestie e insulti."),
    ("Caso di stalking online", "Sorveglianza e molestie attraverso i social media."),
    ("Caso di truffa online", "Sottrazione di denaro tramite siti fraudolenti."),
    ("Caso di violazione di copyright", "Distribuzione illegale di contenuti protetti."),
    ("Caso di DDoS", "Attacco per sovraccaricare i server di un'azienda."),
    ("Caso di frode finanziaria", "Manipolazione di dati per truffe economiche."),
    ("Caso di sextortion", "Ricatti basati su materiale compromettente."),
    ("Caso di violazione della privacy", "Esposizione non autorizzata di dati personali."),
    ("Caso di spyware", "Installazione di software per monitorare attività di un utente."),
    ("Caso di exploit 0-day", "Sfruttamento di vulnerabilità non ancora conosciute."),
    ("Caso di frode su e-commerce", "Acquisti fraudolenti utilizzando carte rubate."),
    ("Caso di pedopornografia online", "Distribuzione di contenuti illegali attraverso il web."),
    ("Caso di furto di dati medici", "Violazione di database contenenti informazioni sanitarie."),
    ("Caso di fake news", "Diffusione di informazioni false per manipolare opinioni."),
    ("Caso di deepfake", "Uso di video manipolati per scopi malevoli."),
    ("Caso di tracciamento non autorizzato", "Monitoraggio di utenti senza consenso."),
    ("Caso di frode tramite criptovalute", "Truffa legata a pagamenti in criptovalute."),
    ("Caso di hacking governativo", "Attacco informatico contro istituzioni pubbliche."),
    ("Caso di child grooming", "Adescamento di minori tramite piattaforme online."),
    ("Caso di revenge hacking", "Attacco informatico per vendetta personale."),
    ("Caso di hacking etico", "Intervento di un hacker per identificare vulnerabilità."),
    ("Caso di spionaggio industriale", "Sottrazione di segreti aziendali da concorrenti."),
]

# Inserimento dei dati nel database
for nome, descrizione in strumenti_data:
    execute_query("INSERT INTO Strumenti (nome, descrizione) VALUES (?, ?)", (nome, descrizione))

for nome, descrizione in procedure_data:
    execute_query("INSERT INTO Procedure (nome, descrizione) VALUES (?, ?)", (nome, descrizione))

for nome, descrizione in normativa_data:
    execute_query("INSERT INTO Normativa (nome, descrizione) VALUES (?, ?)", (nome, descrizione))

for nome, descrizione in casi_data:
    execute_query("INSERT INTO Casi (nome, descrizione) VALUES (?, ?)", (nome, descrizione))

print("Tutti i dati sono stati inseriti correttamente nel database.")