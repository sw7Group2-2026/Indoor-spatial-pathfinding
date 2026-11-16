from .collection_handler import createCollection, populateAttributes, queryResponse

COLLECTION_NAME = "Attributes"

def run():
    # Create the 'Attributes' collection in chroma_db
    attribute_collection = createCollection(COLLECTION_NAME)

    # Populate the collection with room descriptions and feature types from PostGIS
    populateAttributes(attribute_collection)

    # Example ambiguous request
    request = 'Hvor kan man købe mad?'

    # ChromaDB embeds the request and returns the 10 nearest embeddings
    response = queryResponse(attribute_collection, request)

    # Print result
    print(response)
    '''print("Request: " + request)
    print("Response:")
    for documents in response['documents']:
        for document in documents:
            print(document)'''