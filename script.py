from db_utils import fetch_query

# Verifica i dati della tabella "Strumenti"
print(fetch_query("SELECT * FROM Strumenti LIMIT 5"))

# Verifica i dati della tabella "Procedure"
print(fetch_query("SELECT * FROM Procedure LIMIT 5"))

# Verifica i dati della tabella "Normativa"
print(fetch_query("SELECT * FROM Normativa LIMIT 5"))

# Verifica i dati della tabella "Casi"
print(fetch_query("SELECT * FROM Casi LIMIT 5"))
