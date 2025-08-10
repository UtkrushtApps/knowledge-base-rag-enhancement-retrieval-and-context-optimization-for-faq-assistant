import os
import sys

data_dir = '/app/data/'
if not os.path.isdir(data_dir):
    os.makedirs(data_dir, exist_ok=True)
config_dir = '/app/config/'
if not os.path.isdir(config_dir):
    os.makedirs(config_dir, exist_ok=True)

try:
    for pkg in ['chromadb', 'sentence_transformers', 'openai', 'numpy', 'pandas', 'tiktoken']:
        __import__(pkg)
    print("[INIT] Directories and dependencies ready.")
except ImportError as ex:
    sys.exit(f"[ERROR] Missing dependency: {ex}")
