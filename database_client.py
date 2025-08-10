import chromadb
from chromadb.config import Settings
import json

def get_collection():
    with open('config/database.json') as f:
        cfg = json.load(f)
    client = chromadb.Client(Settings(persist_directory=cfg['db_path']))
    return client.get_collection(cfg['collection'])
