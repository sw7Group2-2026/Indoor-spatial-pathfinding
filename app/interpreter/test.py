from .collection_handler import createCollection, populateAttributes, queryResponse
from interpreter.models.llama import Llama

COLLECTION_NAME = "Attributes"

def run():
    # Create the 'Attributes' collection in chroma_db
    # attribute_collection = createCollection(COLLECTION_NAME)

    # Populate the collection with room descriptions and feature types from PostGIS
    # populateAttributes(attribute_collection)

    # Example ambiguous request
    llamaLLM = Llama()
    request = input("Ask about the building: ")
    jsonResponse = llamaLLM.prompt(request)
    print("Test json response:")
    print(jsonResponse)

    '''if jsonResponse.attributes:
        # ChromaDB embeds the request and returns the 10 nearest embeddings
        response = queryResponse(attribute_collection, jsonResponse.attributes)

        print("Request: " + request)
        print("Response:")
        for documents in response['documents']:
            for document in documents:
                print(document)'''