import os
import json
import chromadb
from chromadb.config import Settings
import numpy as np
import tiktoken
import openai

DOC_PATH = '/app/data/documents/'
COLLECTION_NAME = 'faq_collection'
CHUNK_SIZE = 256
CHUNK_OVERLAP = 32
EMBED_DIM = 1536
ENCODER = tiktoken.get_encoding('cl100k_base')

OPENAI_EMBED_MODEL = 'text-embedding-ada-002'
openai.api_key = os.getenv('OPENAI_API_KEY', 'test-api-key')

def tokenize(text):
    return ENCODER.encode(text)

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    toks = tokenize(text)
    idx = 0
    chunks = []
    while idx < len(toks):
        window = toks[idx:idx+size]
        s = ENCODER.decode(window)
        chunks.append((s, idx, len(window)))
        idx += size - overlap
    return chunks

if __name__ == '__main__':
    db_client = chromadb.Client(Settings(persist_directory='/app/data/db/'))
    files = [os.path.join(DOC_PATH, 'faq_data.txt')]
    col = db_client.get_or_create_collection(COLLECTION_NAME)
    embed_texts = []
    metadatas = []
    chunk_count = 0
    for f in files:
        with open(f, 'r', encoding='utf8') as doc:
            doc_txt = doc.read()
        doc_id = os.path.basename(f)
        # Split on numbered FAQ headings for metadata
        faqs = [part.strip() for part in doc_txt.split('\n\n') if part.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.'))]
        for faq in faqs:
            cat = faq.split('.',1)[0] if '.' in faq else ''
            chunks = chunk_text(faq)
            for i, (chunk, start_pos, tok_count) in enumerate(chunks):
                faq_id = f"{cat}_faq_{i}"
                meta = {
                    'doc_id': doc_id,
                    'faq_id': faq_id,
                    'category': cat,
                    'title': faq.split('\n', 1)[0].strip()[:60],
                    'content': chunk,
                    'token_count': tok_count,
                    'chunk_index': i
                }
                embed_texts.append(chunk)
                metadatas.append(meta)
                chunk_count += 1
    # Batch embed
    embeddings = []
    BATCH = 32
    for i in range(0, len(embed_texts), BATCH):
        batch = embed_texts[i:i+BATCH]
        emb = openai.Embedding.create(input=batch, model=OPENAI_EMBED_MODEL)['data']
        for e in emb:
            embeddings.append(e['embedding'])
    for meta, emb in zip(metadatas, embeddings):
        col.add(documents=[meta['content']], metadatas=[meta], ids=[meta['faq_id']], embeddings=[emb])
    print(f"[PROCESS] {len(embeddings)} FAQ chunks inserted.")
