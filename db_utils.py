import sqlite3

DB_FILE = 'procedura_forense.db'  # Nome del file del database

# Funzione per eseguire una query SQL
def execute_query(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# Funzione per ottenere i dati da una query
def fetch_query(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Funzione per creare le tabelle necessarie
def create_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Creazione della tabella Strumenti
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Strumenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descrizione TEXT NOT NULL
    )
    """)

    # Creazione della tabella Procedure
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Procedure (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descrizione TEXT NOT NULL
    )
    """)

    # Creazione della tabella Normativa
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Normativa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descrizione TEXT NOT NULL
    )
    """)

    # Creazione della tabella Casi
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Casi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descrizione TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# Eseguire la creazione delle tabelle
if __name__ == '__main__':
    create_tables()
    print("Tutte le tabelle sono state create correttamente.")
