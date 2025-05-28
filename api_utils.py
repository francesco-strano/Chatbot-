import requests
from settings import API_URL, MODEL_NAME, MAX_TOKENS, TEMPERATURE, MAX_CONTEXT_TOKENS

def tronca_input(messages):
    """
    Tronca i messaggi per rispettare i limiti di token.
    """
    max_tokens = 4096  # Limite massimo di token (ad esempio per GPT-3.5)
    total_tokens = 0
    truncated_messages = []

    for message in messages:
        # Verifica che il contenuto non sia None
        content = message.get("content", "")
        if content is None:
            content = ""

        # Calcola il numero di token approssimati
        message_tokens = len(content.split())
        total_tokens += message_tokens

        # Se si supera il limite, interrompi il ciclo
        if total_tokens > max_tokens:
            break

        truncated_messages.append(message)

    return truncated_messages


def call_api(messages):
    """
    Invia una richiesta all'API del modello di linguaggio.
    :param messages: Lista di messaggi da inviare all'API.
    :return: Risposta elaborata dal modello o messaggio di errore.
    """
    # Verifica se i messaggi sono vuoti
    if not messages:
        return "Errore: La lista 'messages' non può essere vuota."

    print(f"Messaggi prima della troncatura: {messages}")

    # Tronca i messaggi per rispettare il limite di contesto
    messages = tronca_input(messages)

    # Verifica che i messaggi siano ancora presenti dopo la troncatura
    if not messages:
        return "Errore: Nessuna Informazione disponibile per l'elaborazione."

    print(f"Messaggi dopo la troncatura: {messages}")

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE
    }

    headers = {"Content-Type": "application/json"}

    try:
        # Stampa per debug
        print(f"Inviando richiesta a: {API_URL}")
        print(f"Payload: {payload}")

        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()

        # Analizza la risposta
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()
        else:
            return "Errore: Nessuna risposta valida ricevuta dall'API."
    except requests.exceptions.RequestException as e:
        return f"Errore di connessione: {e}"
    except KeyError:
        return "Errore nella risposta dell'API."
