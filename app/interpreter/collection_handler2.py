
import chromadb
from chromadb.utils import embedding_functions
from database.supa_db_handler import SupaDatabaseHandler

CHROMA_PATH = "./interpreter/chroma_db"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


# Creates a collection with sentence-transformer as the embedding function
def createCollection(collectionName):
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

    collection = client.get_or_create_collection(
        name=collectionName,
        embedding_function=embedding_fn
    )

    return collection


# Populate collection with relevant attributes from PostGIS
def populateAttributes(collection):
    db = SupaDatabaseHandler()

    # Get feature types and unique room descriptions
    features = db.query(
        "SELECT feature_type_id, name FROM feature_type;"
    )

    descriptions = db.query(
        "SELECT DISTINCT ON (room_description) "
        "indoor_space_id, room_description "
        "FROM indoor_space "
        "WHERE room_description IS NOT NULL;"
    )

    attributes = []

    # Feature types
    for feature in features:
        name = feature["name"]

        attributes.append({
            "id": f"feat_{feature['feature_type_id']}",
            "document": name.lower(),
            "metadata": {
                "type": "feature",
                "original_name": name
            }
        })

    # Room descriptions
    for description in descriptions:
        name = description["room_description"]

        attributes.append({
            "id": f"desc_{description['indoor_space_id']}",
            "document": name.lower(),
            "metadata": {
                "type": "room description",
                "original_name": name
            }
        })

    # Update existing attributes and their embeddings
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


# Query ChromaDB
def queryResponse(collection, request):

    # Convert all search texts to lowercase
    request = [text.lower() for text in request]

    response = collection.query(
        query_texts=request,
        include=["documents", "metadatas", "distances"],
        n_results=5
    )

    return response


def findBestMatch(collection, attributes):
    # Split Llama attributes into separate words
    search_words = [
        word.strip()
        for word in attributes.split(",")
        if word.strip()
    ]

    if not search_words:
        return None

    # Search each word in ChromaDB
    response = queryResponse(collection, search_words)

    best_match = None
    best_distance = float("inf")

    # Compare all results
    for documents, distances, metadatas in zip(
        response["documents"],
        response["distances"],
        response["metadatas"]
    ):
        for document, distance, metadata in zip(
            documents, distances, metadatas
        ):
            if distance < best_distance:
                best_distance = distance
                best_match = {
                    "name": metadata.get("original_name", document),
                    "distance": distance,
                    "type": metadata.get("type")
                }

    return best_match