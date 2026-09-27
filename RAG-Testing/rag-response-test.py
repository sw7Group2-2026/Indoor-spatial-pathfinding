from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import os

current = Path(__file__).resolve().parent
CHROMA_PATH = str(current / "chroma_db")
COLLECTION_NAME = "Rooms"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

client = chromadb.PersistentClient(path=CHROMA_PATH)
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

collection = client.get_collection(COLLECTION_NAME,embedding_fn)



results = collection.query(
    query_texts=["where is the toilets"],
    include=["documents", "metadatas", "embeddings"],
)
print(results["metadatas"][0][0])