import chromadb
from chromadb.utils import embedding_functions
from database.supa_db_handler import SupaDatabaseHandler
from dotenv import load_dotenv
from pathlib import Path
import os

CURRENT_PATH = Path(__file__).resolve().parent
CHROMA_PATH = str(CURRENT_PATH / "chroma_db")
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
BATCH_SIZE = 100

class CollectionHandler:
    def __init__(
        self,
        collection_name,
        embedding_model: str = EMBEDDING_MODEL,
        batch_size: int = 100
    ):
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.batch_size = batch_size

        load_dotenv()

        self.client = chromadb.PersistentClient(path=CHROMA_PATH)

        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.embedding_model
        )
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn,
        )

    def deleteCollection(self):
        self.client.delete_collection(name=self.collection_name)

    def printCollection(collectionName):
        pass

    # Populate collection with relevant attributes from PostGIS
    def populateAttributes(self):
        # Create Supabase database handler object
        db = SupaDatabaseHandler()

        # Get feature types and (unique+non-null) room descriptions
        features = (
            db.query(
                """
                SELECT feature_type_id, name 
                FROM feature_type_e;
                """
            )
        )
        descriptions = (
            db.query(
                """
                SELECT DISTINCT ON (room_description) indoor_space_id, room_description 
                FROM indoor_space_e 
                WHERE room_description IS NOT NULL;
                """
            )
        )

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

        for i in range(0, len(attributes), BATCH_SIZE):
            batch = attributes[i : i + BATCH_SIZE]
            self.collection.upsert(
                ids=[item["id"] for item in batch],
                documents=[item["document"] for item in batch],
                metadatas=[item["metadata"] for item in batch],
            )

        # Upsert (insert or update) these attributes in the collection
        if attributes:
            print(f"Successfully updated {len(attributes)} items in ChromaDB.")
        else:
            print("No attributes found to sync.")

        return attributes

    # Queries the vector database in the specified collection with the specified request
    def queryResponse(self, request):
        response = self.collection.query(
                query_texts=request,
                include=["documents", "distances"],
                n_results=5
            )
        return response