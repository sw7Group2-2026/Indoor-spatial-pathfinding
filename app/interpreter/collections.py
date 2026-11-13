import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = ("./app/interpreter/chroma_db")
COLLECTION_NAME = "Attributes"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

client = chromadb.PersistentClient( path = CHROMA_PATH )

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction( model_name = EMBEDDING_MODEL )

collection = client.get_or_create_collection(
    name = COLLECTION_NAME,
    embedding_function = embedding_fn,
    metadata = { 
        description = "Known attributes of either feature types or room descriptions." 
        }
)

### TODO: GET LIST OF PAIRS (ID, NAME) FOR FEATURE AND ROOM DESCRIPTION
# features = "SELECT feature_type_id, name FROM feature_type"
# descriptions = "SELECT room_description_id, room_description FROM indoor_space"

attributes = []

for feature in features:
    attributes.append({
        "id": f"feat_{feature.id}",
        "document": feature.name,
        "metadata": {"type": "feature"}
    })

for desc in descriptions:
    attributes.append({
        "id": f"desc_{description.id}",
        "document": description.name,
        "metadata": {"type": "room description"}
    })

if attributes:
    collection.upsert(
        ids=[attr["id"] for attr in attributes],
        documents=[attr["document"] for attr in attributes],
        metadatas=[attr["metadata"] for attr in attributes]
    )
    print(f"Successfully updated {len(attributes)} items in ChromaDB.")
else:
    print("No attributes found to sync.")