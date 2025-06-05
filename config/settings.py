import os
from dotenv import load_dotenv

load_dotenv()

API_ID_STR = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

API_ID = None
if API_ID_STR:
    try:
        API_ID = int(API_ID_STR)
    except ValueError:
        print(f"Kesalahan: API_ID '{API_ID_STR}' bukan angka yang valid.")
        exit(1)
else:
    print("Kesalahan: API_ID tidak ditemukan di .env")
    exit(1)

if not all([API_HASH, GEMINI_API_KEY, SUPABASE_URL, SUPABASE_KEY, PHONE_NUMBER]):
    print("Kesalahan: Pastikan semua variabel lingkungan (API_HASH, GEMINI_API_KEY, SUPABASE_URL, SUPABASE_KEY, PHONE_NUMBER) telah diatur di file .env.")
    exit(1)


GEMINI_MODEL_NAME = "gemini-2.0-flash" 
GEMINI_MAX_OUTPUT_TOKENS = 1000
GEMINI_TEMPERATURE = 0.7
GEMINI_TOP_P = 1.0
GEMINI_TOP_K = 1
CONVERSATION_HISTORY_LIMIT = 6
GEMINI_SYSTEM_PROMPT = "Nama kamu adalah idkyuyet dan kamu laki laki berumur 20 tahun dan kamu memiliki gaya bahasa yang cuek dan menjawab maksimal 5 kata dan kamu juga memiliki sifat yang peduli. pakai aku, kamu, jangan gue elu" 

GEMINI_SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
