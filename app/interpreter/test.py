from interpreter.collection_handler import CollectionHandler
from interpreter.models.llama import Llama

COLLECTION_NAME = "Attributes"

def run():
    collection = CollectionHandler(COLLECTION_NAME)
    # Populate the collection with room descriptions and feature types from PostGIS
    attributes = collection.populateAttributes()
    print(attributes)
    # deleteCollection(COLLECTION_NAME)

    # Example ambiguous request
    llamaLLM = Llama()
    request = input("Ask about the building: ")
    jsonResponse = llamaLLM.prompt(request)
    print("Test json response:")
    print(jsonResponse)

    if jsonResponse["attributes"]:
        # ChromaDB embeds the request and returns the 10 nearest embeddings
        response = collection.queryResponse(jsonResponse["attributes"])

        print("Request: " + request)
        print("Response:")
        for documents in response['documents']:
            for document in documents:
                print(document)