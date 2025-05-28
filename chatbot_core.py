import streamlit as st
from fpdf import FPDF
from db_utils import fetch_query

def salva_risposte_forensi(domanda, risposta):
    st.session_state["domande_risposte"].append({"domanda": domanda, "risposta": risposta})

def genera_relazione_tecnica_pdf():
    if not st.session_state["domande_risposte"]:
        st.warning("Nessuna risposta disponibile per generare la relazione.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Relazione Tecnica Forense", ln=True, align="C")
    pdf.ln(10)

    for item in st.session_state["domande_risposte"]:
        domanda = item["domanda"]
        risposta = item["risposta"]
        pdf.multi_cell(0, 10, f"Domanda: {domanda}\nRisposta: {risposta}")
        pdf.ln(5)

    file_name = "Relazione_Tecnica_Forense.pdf"
    pdf.output(file_name)
    st.success("Relazione creata con successo!")
    with open(file_name, "rb") as file:
        st.download_button("📥 Scarica la Relazione in PDF", file, file_name=file_name)

def mostra_record(tabella):
    query = f"SELECT * FROM {tabella} ORDER BY RANDOM() LIMIT 5"
    risultati = fetch_query(query)
    if risultati:
        for record in risultati:
            st.write(f"Nome: {record[1]}, Descrizione: {record[2]}")
    else:
        st.warning(f"Nessun record trovato nella tabella {tabella}.")

def analizza_file_allegato(file):
    """
    Analizza un file allegato e restituisce una sintesi.
    """
    try:
        # Simulazione dell'analisi del file
        nome_file = file.name
        contenuto = file.read().decode('utf-8') if file.type == 'text/plain' else "[Contenuto binario non leggibile]"

        # Restituisce un riassunto semplice
        return f"Analisi del file '{nome_file}':\n{contenuto[:200]}..."
    except Exception as e:
        return f"Errore nell'analisi del file '{file.name}': {e}"
