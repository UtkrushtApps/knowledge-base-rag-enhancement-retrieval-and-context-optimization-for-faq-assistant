import chromadb
from chromadb.config import Settings
COLLECTION_NAME = 'faq_collection'
client = chromadb.Client(Settings(persist_directory='/app/data/db/'))
try:
    col = client.get_collection(COLLECTION_NAME)
    count = col.count()
    ex = col.peek(2)
    print(f"[VERIFY] Collection '{COLLECTION_NAME}': {count} chunks ready.")
    print(f"[VERIFY] Sample metadata: {ex['metadatas'][0]}")
    print(f"[VERIFY] Sample FAQ: {ex['documents'][0][:120]}")
    print("[VERIFIED] FAQ vector DB operational.")
except Exception as e:
    print(f"[ERROR] Verification failed: {e}")
    exit(1)
