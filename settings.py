# URL dell'API per il modello di linguaggio
API_URL = "http://127.0.0.1:1234/v1/chat/completions"

# Configurazioni del modello
MODEL_NAME = "llama-3.2-1b-instruct"  # Nome del modello utilizzato
MAX_TOKENS = 5000  # Numero massimo di token generabili nella risposta
TEMPERATURE = 0.7  # Creatività del modello (0.0 = deterministico, 1.0 = più creativo)

# Limite massimo di token per il contesto
MAX_CONTEXT_TOKENS = 4096

# Debug mode (True per attivare log di debug)
DEBUG_MODE = True
