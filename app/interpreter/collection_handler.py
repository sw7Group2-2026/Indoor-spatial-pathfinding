import chromadb
from chromadb.utils import embedding_functions
from database.supa_db_handler import SupaDatabaseHandler

CHROMA_PATH = ("./interpreter/chroma_db")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Creates a new collection with sentence-transformer as the embedding function
def createCollection(collectionName):
    client = chromadb.PersistentClient( path = CHROMA_PATH )

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction( model_name = EMBEDDING_MODEL )

    collection = client.get_or_create_collection(
        name = collectionName,
        embedding_function = embedding_fn
    )

    return collection

# Populate collection with relevant attributes from PostGIS
def populateAttributes(collection):
    # Create Supabase database handler object
    db = SupaDatabaseHandler()

    # Get feature types and (unique/non-null) room descriptions
    features = db.query("SELECT feature_type_id, name FROM feature_type;")
    descriptions = db.query("SELECT DISTINCT ON (room_description) indoor_space_id, room_description FROM indoor_space WHERE room_description IS NOT NULL;")

    # Empty attribute list
    attributes = []

    # Append feature type data to attribute list
    for feature in features:
        attributes.append({
            "id": f"feat_{feature['feature_type_id']}",
            "document": feature['name'],
            "metadata": {"type": "feature"}
        })

    # Append room description data to attribute list
    for description in descriptions:
        attributes.append({
            "id": f"desc_{description['indoor_space_id']}",
            "document": description['room_description'],
            "metadata": {"type": "room description"}
        })

    # Upsert (insert or update) these attributes in the collection
    if attributes:
        collection.upsert(
            ids=[attr["id"] for attr in attributes],
            documents=[attr["document"] for attr in attributes],
            metadatas=[attr["metadata"] for attr in attributes]
        )
        print(f"Successfully updated {len(attributes)} items in ChromaDB.")
    else:
        print("No attributes found to sync.")

    return attributes

# Queries the vector database in the specified collection with the specified request
def queryResponse(collection, request):
    response = collection.query(
            query_texts=[request]
        )
    return response