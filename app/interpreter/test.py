from interpreter.collection_handler import CollectionHandler
from interpreter.models.llama import Llama
from interpreter.user_query import UserQuery

# Name of the collection
COLLECTION_NAME = "Attributes"

# Constants for the initial LLM layer
PROMPT_ENGINEERING_INPUT = "prompt_engineering1.txt"
RESPONSE_FORMAT_INPUT = UserQuery.getJson()

# Constants for the validartion LLM layer
PROMPT_ENGINEERING_VALIDATION = "prompt_engineering2.txt"
RESPONSE_FORMAT_VALIDATION = {
    "type": "object",
    "properties": {
        "attributes": {
            "type": "array",
            "items": {"type": "string"},
        }
    },
    "required": ["attributes"],
}

def run():
    # Create the Attributes collection
    collection = CollectionHandler(COLLECTION_NAME)
    
    # Populate collection with data from PostGIS
    collection.populateAttributes()

    # Create instance of LLM and prompt an input from the user
    llamaLLM = Llama()
    userInput = input("Ask about the building: ")

    # LLM initial layer: Generate a structured output extracted from the user input
    jsonResponse = llamaLLM.prompt(
        userInput, 
        PROMPT_ENGINEERING_INPUT, 
        RESPONSE_FORMAT_INPUT
    )

    # Debug: Print the structured output for testing (JSON)
    print("\nTest json response:")
    print(jsonResponse)

    # If any attribute keywords are found, find actual attributes in vector DB
    if jsonResponse["attributes"]:

        # Convert attributes from comma-separated string into list
        attributes = [
            word.strip()
            for word in jsonResponse["attributes"].split(",")
            if word.strip()
        ]

        # Search for each attribute separately in ChromaDB
        response = collection.queryResponse(attributes)

        # Printing response + distances for testing
        print("\nRequest:", userInput)
        print("Response:")

        for word, documents, distances in zip(
            attributes,
            response["documents"],
            response["distances"]
        ):
            print(f"\nSøgning: {word}")

            for document, distance in zip(documents, distances):
                print(f"{document}: {distance:.4f}")

        # Put all ChromaDB results into one list
        response_docs = [doc for docs in response["documents"] for doc in docs]
        print("Response docs:")
        print(response_docs)

        #Combine the original question and ChromaDB results for Llama2
        prompt = f'''User: {userInput}, Results:{", ".join(response_docs)}'''

        # LLM verification layer: 
        # Check which results actually match the user's question
        verified_response = llamaLLM.prompt(
            prompt,
            PROMPT_ENGINEERING_VALIDATION,
            RESPONSE_FORMAT_VALIDATION
        )

        print("\nLLM verification:")
        print(verified_response)


    else:
        print("No attributes to search for.")