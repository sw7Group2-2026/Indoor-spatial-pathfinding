from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import os

current = Path(__file__).resolve()

CHROMA_PATH = os.path.join(current, "chroma_db") 
COLLECTION_NAME = "Rooms"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

class Room():
    def __init__(self,roomID, utilities,description):
        self.roomID = roomID
        self.utilities = utilities
        self.description = description
        self.querry = "shortes.path.room(" + self.roomID +")"


rooms: list = [Room("2.2.042",["TV","Table","Power"],"study room for students at software sudents at 7th semester."), 
               Room("2.2.041",["TV","Table","Power"],"study room for students at software sudents at 7th semester."), 
               Room("2.2.040",["TV","Table","Power"],"study room for students at software sudents at 7th semester."), 
               Room("2.2.038",["Toilet","Sink","Paper"],"Male and female toilets and sanitation.")]


client = chromadb.PersistentClient(path=CHROMA_PATH)

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

try:
    client.delete_collection(COLLECTION_NAME)
    print(f"Deleted existing collection: {COLLECTION_NAME}")
except Exception:
    print("No existing collection found")

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn,
    metadata={"description": "Rooms and there context"},
)

ids = [room.roomID for room in rooms]
documents = [room.description + room.utilities for room in rooms]
metadatas = [room for room in rooms]

batch_size = 100
for i in range(0, len(ids), batch_size):
    collection.add(
    ids=ids[i:i + batch_size],
    documents=documents[i:i + batch_size],
    metadatas=metadatas[i:i + batch_size],
)