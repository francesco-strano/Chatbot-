import os
import unicodedata
import streamlit as st
from PyPDF2 import PdfReader
from fpdf import FPDF
import tempfile
from api_utils import call_api  # Importa la funzione API dal file api_utils

# Percorso delle relazioni di riferimento
PERCORSO_RELAZIONI = r"C:\\Users\\stran\\OneDrive\\Desktop\\prove\\Esempi Relazioni tecniche"

# Template della relazione
TEMPLATE_RELAZIONE = """
Relazione Tecnica

**Introduzione**
{introduzione}

**Dati**
{contesto}

**Mezzi e Procedure**
{strumenti_metodologie}

**Risultati**
{risultati}

**Conclusioni e Raccomandazioni**
{conclusioni}

"""

# Inizializza lo stato della sessione
def init_session_state():
    chiavi_da_inizializzare = {
        "bozza": "",
        "file_allegati": [],
        "chat": [],
        "nome_file_pdf": None
    }
    for chiave, valore in chiavi_da_inizializzare.items():
        if chiave not in st.session_state:
            st.session_state[chiave] = valore
def genera_pdf_domande_risposte(domande, risposte):
    file_path = "risposte_relazione_tecnica.pdf"
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Risposte alla Relazione Tecnica", ln=True, align="C")
    pdf.ln(10)

    for domanda, risposta in zip(domande, risposte):
        pdf.set_font("Arial", style="B", size=11)
        pdf.multi_cell(0, 10, domanda)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 10, risposta if risposta else "Nessuna risposta fornita.")
        pdf.ln(5)

    try:
        pdf.output(file_path)
        return file_path
    except Exception as e:
        st.error(f"Errore durante la creazione del PDF: {e}")
        return None


def mostra_domande():
    st.markdown("## 📄 Creazione Relazione Tecnica Forense")

    # Definizione delle domande
    domande = [
        "Quali strumenti tecnici e metodologie forensi sono stati impiegati?",
        "Quali procedure standard sono state seguite durante l'indagine?",
        "Quali normative sono state rispettate?",
        "Quali evidenze chiave sono state raccolte e come sono state verificate?",
        "Qual è stata la timeline delle operazioni forensi?",
        "Quali misure di sicurezza sono state adottate per proteggere l'integrità dei dati?"
    ]

    # Inizializzazione dello stato della sessione
    if "risposte" not in st.session_state:
        st.session_state["risposte"] = [""] * len(domande)

    if "relazione_completa" not in st.session_state:
        st.session_state["relazione_completa"] = ""

    # Input dell'utente per ogni domanda
    for i, domanda in enumerate(domande):
        st.markdown(f"### {domanda}")
        risposta_utente = st.text_area(
            label=f"Risposta {i+1}",
            value=st.session_state["risposte"][i],
            key=f"risposta_{i}",
            label_visibility="hidden"
        )
        st.session_state["risposte"][i] = risposta_utente

    # Generazione della relazione arricchita
    if st.button("📌 Genera Relazione Professionale"):
        relazione_finale = call_api([
            {
                "role": "system",
                "content": (
                        "Sei un esperto in analisi forense e redazione tecnica. Il tuo compito è redigere una relazione forense dettagliata, "
                        "formale e ben strutturata basandoti esclusivamente sulle risposte dell’utente. "
                        "Assicurati di seguire una struttura chiara e logica con le seguenti sezioni:\n"
                        "- **Introduzione**: descrivi il contesto generale dell’indagine.\n"
                        "- **Metodologia**: spiega le tecniche e strumenti utilizzati, giustificandone l’uso.\n"
                        "- **Analisi dei dati**: esamina i risultati, facendo riferimenti a normative pertinenti.\n"
                        "- **Conclusioni e raccomandazioni**: riassumi le evidenze e suggerisci azioni future.\n"
                        "Evita di riportare queste istruzioni nel testo finale. "
                        "Per ogni risposta dell’utente, arricchisci il contenuto con dettagli tecnici e riferimenti normativi pertinenti. "
                        "Se possibile, includi esempi di casi simili o best practices. "
                        "La relazione deve essere di almeno 2000 parole e mantenere un tono professionale e chiaro."
                        "controlla che le risposte siano complete e coerenti con le domande."
                        "Consigli per la redazione: utilizza un linguaggio formale e tecnico, evita espressioni colloquiali o informali."
                        "Conclusioni e raccomandazioni: sii chiaro e conciso, fornendo indicazioni specifiche e misure correttive."
                        "Ricorda di includere riferimenti normativi e best practices per supportare le tue conclusioni."
                        "assicurati che la relazione sia ben strutturata e coerente, con una chiara sequenza logica dei contenuti."
                        
            
                )
            },
            {
                "role": "user",
                "content": "\n".join(
                    f"{domande[i]} {st.session_state['risposte'][i]}" if st.session_state["risposte"][i].strip() else ""
                    for i in range(len(domande))
                )
            }
        ]).strip()

        st.session_state["relazione_completa"] = relazione_finale

        # Mostra la relazione arricchita
        st.markdown("## ✍ Relazione Generata")
        st.session_state["relazione_completa"] = st.text_area(
            label="Modifica la relazione",
            value=relazione_finale,
            height=400
        )

    # Generazione del PDF con la relazione completa
    if st.button("📥 Scarica Relazione in PDF"):
        nome_file = genera_relazione_tecnica_pdf(st.session_state["relazione_completa"])
        if nome_file:
            with open(nome_file, "rb") as file:
                st.download_button(
                    label="📄 Scarica il PDF",
                    data=file,
                    file_name="Relazione_Tecnica_Forense.pdf",
                    mime="application/pdf"
                )



# Normalizza il testo per evitare errori di codifica
def normalizza_testo(testo):
    return unicodedata.normalize("NFKD", testo).encode("ascii", "ignore").decode("ascii")

# Leggi i contenuti dal percorso relazioni
def leggi_contenuti_extra(percorso):
    contenuti = []
    try:
        for file in os.listdir(percorso):
            percorso_file = os.path.join(percorso, file)
            if os.path.isfile(percorso_file):
                with open(percorso_file, 'r', encoding='utf-8') as f:
                    contenuti.append(f.read())
        return "\n\n".join(contenuti)
    except Exception as e:
        return f"Errore durante la lettura dei contenuti extra: {str(e)}"
    
    # Modalità Chatbot Normale
def chat_normale(user_input):
    # Prepara i messaggi
    messages = [{"role": "user", "content": user_input}]
    try:
        bot_response = call_api(messages)
        st.session_state['active_chat'].append({"role": "assistant", "content": bot_response})
        st.chat_message("assistant").markdown(bot_response)
    except Exception as e:
        st.error(f"Errore durante la comunicazione con l'API: {e}")

# Analizza i file allegati e utilizza l'API per generare contenuti
def analizza_file_e_genera(file):
    try:
        reader = PdfReader(file)
        contenuto_file = "".join([page.extract_text() for page in reader.pages])

        # Preparare il payload
        payload = [
            {"role": "system", "content": "Sei un assistente esperto nella creazione di relazioni tecniche forensi."},
            {"role": "user", "content": f"Genera una relazione completa basata sul seguente contenuto:\n\n{contenuto_file}"}
        ]

        # Chiamata al modello API
        try:
            informazioni_aggiuntive = call_api(payload)
        except Exception as api_error:
            informazioni_aggiuntive = (
                "Non è stato possibile generare informazioni aggiuntive tramite l'API. "
                "Controlla la connessione o il server API.\n"
                f"Errore: {api_error}"
            )

        # Struttura della relazione
        introduzione = "Questa relazione tecnica è stata generata per analizzare il file allegato."
        contesto = f"Il file allegato contiene informazioni relative a: {contenuto_file[:5000]}..."
        strumenti_metodologie = "Gli strumenti utilizzati includono tecniche avanzate di analisi forense."
       # evidenze = f"Dati estratti dal file:\n\n{contenuto_file[:5000]}..."
        risultati = "L’analisi forense ha consentito di ottenere informazioni tecniche e dettagli significativi dal materiale video esaminato. Sono stati identificati aspetti fondamentali relativi alla dinamica del crimine, alle caratteristiche fisiche e ai comportamenti dei soggetti coinvolti, nonché ai metodi utilizzati per l’esecuzione del reato."
        conclusioni = "L’analisi forense ha permesso di ricostruire la dinamica del crimine e ottenere dettagli utili alle indagini, sebbene la qualità video e l’uso di camuffamenti abbiano limitato l’identificazione certa. Si raccomanda l’uso di telecamere ad alta risoluzione e l’integrazione con altre fonti di prova per migliorare l'efficacia delle analisi future."
        #contenuti_extra = leggi_contenuti_extra(PERCORSO_RELAZIONI)

        # Restituisci la relazione completa
        return TEMPLATE_RELAZIONE.format(
            introduzione=introduzione,
            contesto=contesto,
            strumenti_metodologie=strumenti_metodologie,
           # evidenze=evidenze,
            risultati=risultati,
            conclusioni=conclusioni,
        )
    except Exception as e:
        return f"Errore durante l'analisi del file: {str(e)}"

# Funzione per salvare il PDF con supporto Unicode
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)  # Aggiungi un font Unicode
        self.set_font('DejaVu', size=12)

    def aggiungi_testo(self, testo):
        for linea in testo.split("\n"):
            self.multi_cell(0, 10, linea)

def genera_relazione_tecnica_pdf(bozza):
    """
    Genera il file PDF per la relazione tecnica forense.
    """
    directory = r"C:\Users\stran\OneDrive\Desktop\tesi seria"
    file_name = "Relazione_Tecnica_Forense.pdf"
    file_path = os.path.join(directory, file_name)

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Crea un oggetto PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Usa un font TrueType (ad esempio, Arial Unicode MS)
    pdf.add_font('Arial', '', r'C:\WINDOWS\FONTS\ARIAL.TTF', uni=True)
    pdf.set_font('Arial', size=12)

    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(0, 10, "Relazione Tecnica Forense", ln=True, align="C")
    pdf.ln(10)

    # Elimina duplicati prima di inserire i dati
    unique_entries = {f"{item['domanda']}|{item['risposta']}" for item in st.session_state.get('domande_risposte', [])}
    for entry in unique_entries:
        domanda, risposta = entry.split("|")
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(0, 10, domanda, ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, risposta)
        pdf.ln(5)

    # Aggiungi la bozza alla fine del PDF
    if bozza:
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(0, 10, "Bozza:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, bozza)
        pdf.ln(5)

    try:
        pdf.output(file_path)
        return file_path
    except Exception as e:
        st.error(f"Errore durante il salvataggio del PDF: {e}")
        return None


def mostra_bozza():
    if st.session_state.get("bozza") and st.session_state.get("generazione_relazione", False):
        st.markdown("### Modifica la Bozza della Relazione")
        nuova_bozza = st.text_area("Relazione Tecnica:", value=st.session_state["bozza"], height=400)
        st.session_state["bozza"] = nuova_bozza

        # Pulsante per salvare il PDF
        if st.button("Salva PDF"):
            nome_file_pdf = genera_relazione_tecnica_pdf(st.session_state["bozza"])
            if nome_file_pdf:
                st.session_state["nome_file_pdf"] = nome_file_pdf
                st.success("PDF salvato con successo!")
            else:
                st.error("Errore durante il salvataggio del PDF.")

        # Controllo che il file PDF esista prima di aggiungere il pulsante di download
        if st.session_state.get("nome_file_pdf"):
            with open(st.session_state["nome_file_pdf"], "rb") as file:
                st.download_button(
                    label="Scarica PDF",
                    data=file,
                    file_name="relazione_tecnica.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("Nessun PDF generato. Salva il PDF prima di scaricarlo.")

# Main
def main():
    init_session_state()

    # Barra laterale 
    st.sidebar.title("🤖 Chatbot Forense")
    st.sidebar.markdown("Genera Relazioni Tecniche Forensi")
   
    st.sidebar.title("🔧 Opzioni")
    st.sidebar.markdown("---")
    st.sidebar.title("Carica File Allegati")
    uploaded_files = st.sidebar.file_uploader("Carica i file per l'analisi", accept_multiple_files=True)
    if uploaded_files:
        st.session_state["file_allegati"].extend(uploaded_files)
        st.sidebar.success(f"{len(uploaded_files)} file caricati con successo!")

    # Pulsante NUOVA CHAT
    if st.sidebar.button("Nuova Chat"):
        st.session_state["chat"] = []
        st.rerun()

    # Reset delle variabili di stato
    if st.sidebar.button("Resetta Tutto"):
        for chiave in st.session_state.keys():
            del st.session_state[chiave]
        st.rerun()

    st.sidebar.title("📌 Comandi Disponibili")
    st.sidebar.info(
        "- **dal file allegato creami una nuova relazione forense** 📄\n"
        "  → Genera automaticamente una relazione partendo da un file PDF.\n\n"
        "- **voglio una relazione tecnica forense** 📝\n"
        "  → Ti guiderà con domande per creare una relazione personalizzata."
    )
# Input utente
user_input = st.chat_input("Scrivi qui... (Es. Dal file allegato creami una nuova relazione forense)")
if user_input:
    if user_input.lower() == "dal file allegato creami una nuova relazione forense":
        if not st.session_state["file_allegati"]:
            st.warning("Carica almeno un file per generare una relazione.")
        else:
            st.session_state["bozza"] = analizza_file_e_genera(st.session_state["file_allegati"][0])
            st.session_state["generazione_relazione"] = True
            st.success("Bozza generata con successo!")

    elif user_input.lower() == "voglio una relazione tecnica forense":
        st.session_state["mostra_domande"] = True
        st.success("Rispondi alle seguenti domande per generare la relazione.")

    else:
        payload = [
            {"role": "system", "content": "Sei un assistente virtuale con conoscenze generali."},
            {"role": "user", "content": user_input}
        ]
        risposta = call_api(payload)
        st.chat_message("assistant").write(risposta)

# Mostra le domande se l'utente ha scritto "voglio una relazione tecnica forense"
if st.session_state.get("mostra_domande", False):
    mostra_domande()

# Mostra la bozza e opzioni di salvataggio/scaricamento
mostra_bozza()

if __name__ == "__main__":
    main()
