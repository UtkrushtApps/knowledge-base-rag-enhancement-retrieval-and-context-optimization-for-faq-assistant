# Knowledge Base RAG Enhancement Task

## Task Overview
You're working on a semantic FAQ assistant that leverages a pre-built Chroma vector database of embedded FAQs. While database and embedding setup are fully automated, the RAG (Retrieval-Augmented Generation) logic remains incomplete. Your role is to finish this logic so the assistant can accurately and concisely answer user queries with properly cited references and efficient context assembly.

## Guidance
- Candidate needs to improve retrieval outcomes — current responses are generic and sometimes irrelevant due to context dilution or poorly constructed prompts.
- Missing logic for query encoding, retrieval (top-k), context building with citation markers, and prompt assembly for downstream LLM.
- System must respect GPT context/token window: use tiktoken for budgeting and avoid overlong prompts.
- Citation markers (e.g., [1], [2]) must align facts in the answer to their retrieved sources.
- You do not need to change or rebuild any vector database code or embedding pipeline; focus exclusively on RAG logic.
- Retrieval quality should be logged (ecall, latency, top-k hit count). Consider a basic filter for FAQ category if included in metadata.

## Database Access
- **Chroma DB** runs in Docker container, reachable as `faq-chroma` on port 8000.
- Main collection: `faq_collection` (already filled with FAQ chunks/embeddings using OpenAI model, dimension=1536).
- Chunk metadata: `doc_id`, `faq_id`, `category`, `title`, `content`, `token_count`, `chunk_index`.
- Access via Chroma Python SDK (see `database_client.py`).
- Explore with database client functions to preview chunks and metadata for debugging.

## Objectives
- Complete the RAG pipeline by:
  - Encoding incoming queries using the same embedding model as stored vectors (OpenAI embeddings provided by stub/API function).
  - Performing top-k vector similarity search using cosine or dot-product similarity.
  - Building a context window of FAQ answers with citation markers (e.g., [1], [2], ...), keeping total prompt under model context window (e.g., 4096 tokens) — use tiktoken to budget.
  - Assembling the final system/user prompt for the LLM including citation notation.
  - Logging retrieval and generation latency and token usage stats to console or log file.
- Optionally, implement a simple filter (by FAQ category) if metadata is present.
- Test your implementation using the provided queries and check that responses contain correct, cited answer spans.

## How to Verify
- Use the queries in `sample_queries.txt` (or your own) against the `/faq-rag/query` endpoint.
- Check output for relevance, response completeness, matching citation markers, and adherence to token window.
- Latency and token statistics should print on each request.
- Spot-check context builder for correct cutoff at token limit and accurate prompt assembly.
