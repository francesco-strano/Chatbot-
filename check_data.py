from db_utils import fetch_query

# Verifica i dati nella tabella Strumenti
query = "SELECT * FROM Procedure"
result = fetch_query(query)

print("Dati nella tabella Procedure:")
for row in result:
    print(row)
