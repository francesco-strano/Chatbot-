import sqlite3

DB_FILE = 'procedura_forense.db'

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Controlla il contenuto delle tabelle
tabelle = ["Procedure", "Strumenti", "Normativa", "Casi"]

for tabella in tabelle:
    print(f"Contenuto della tabella {tabella}:")
    cursor.execute(f"SELECT * FROM {tabella}")
    righe = cursor.fetchall()
    if righe:
        for riga in righe:
            print(riga)
    else:
        print("Nessun dato trovato.")
    print()

conn.close()
