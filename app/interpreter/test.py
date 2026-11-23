from interpreter.collection_handler import CollectionHandler
from interpreter.models.llama import Llama

COLLECTION_NAME = "Attributes"


def run():
    # Create the Attributes collection
    collection = CollectionHandler(COLLECTION_NAME)

    # Populate collection with data from PostGIS
    attributes = collection.populateAttributes()
    print("\nAlle attributter i ChromaDB:")

    print(attributes)

    # TEST 1: Search individual words
    print("\nTEST 1: CHROMADB SEARCH")

    for word in ["kantine", "cafeteria", "restaurant"]:
        response = collection.queryResponse([word])

        print(f"\nSøgning: {word}")

        for document, distance in zip(
            response["documents"][0],
            response["distances"][0]
        ):
            print(f"{document}: {distance:.4f}")

    # TEST 2: Llama + ChromaDB
    print("\nTEST 2: LLAMA + CHROMADB")

    llamaLLM = Llama()
    request = input("Ask about the building: ")

    jsonResponse = llamaLLM.prompt(request)

    print("\nTest json response:")
    print(jsonResponse)

    if jsonResponse["attributes"]:

        # Split Llama attributes into separate search words
        attributes = [
            word.strip()
            for word in jsonResponse["attributes"].split(",")
            if word.strip()
        ]

        # Search for each attribute separately
        response = collection.queryResponse(
            attributes
        )

        print("\nRequest:", request)
        print("Response:")

        for word, documents, distances in zip(
            attributes,
            response["documents"],
            response["distances"]
        ):
            print(f"\nSøgning: {word}")

            for document, distance in zip(documents, distances):
                print(f"{document}: {distance:.4f}")

                            # TEST 3: Llama verifies ChromaDB results
        verified_response = llamaLLM.verify(
            request,
            response["documents"]
        )

        print("\nLLM verification:")
        print(verified_response)


    else:
        print("No attributes to search for.")

