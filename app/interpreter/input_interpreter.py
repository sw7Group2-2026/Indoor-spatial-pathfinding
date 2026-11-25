from dataclasses import dataclass
from interpreter.collection_handler import CollectionHandler
from interpreter.models.llama import Llama
from interpreter.json_schemas import UserQuery, ValidAttributes

# Constants for the collection and its embedding model
COLLECTION_NAME = "Attributes"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
BATCH_SIZE = 100

# Constants for initial LLM layer
PROMPT_ENGINEERING_INPUT = "prompt_engineering1.txt"
RESPONSE_FORMAT_INPUT = UserQuery.getJson()

# Constants for verification LLM layer
PROMPT_ENGINEERING_VALIDATION = "prompt_engineering2.txt"
RESPONSE_FORMAT_VALIDATION = ValidAttributes.getJson()

# Dataclass used to return the data extracted from the user's output
@dataclass
class QueryResult:
    room_number: str | None = None
    building_name: str | None = None
    address: str | None = None
    floor_number: int | None = None
    accessibility: bool = False
    feature_type: list[str] | None = None
    room_description: list[str] | None = None

# Interpreter object with a debug flag for printing intermediate steps
class InputInterpreter:
    def __init__(self, debug = False):
        # Set debug flag
        self.debug = debug

        # Create and populate collection
        self.collection = CollectionHandler(COLLECTION_NAME, EMBEDDING_MODEL, BATCH_SIZE)
        self.collection.populate_attributes()
    
        # Create instance of Llama LLM
        self.llamaLLM = Llama()

    # Main query method. Takes the user input and returns a QueryResult object
    def query(self, user_input):
        # Get structured output from user's input using internal method
        structured_output = self._initial_LLM(user_input)

        if self.debug:
            print("\n Step 1: Initial LLM response:", structured_output, type(structured_output))

        # Populate QueryResult with information from structured output
        result = QueryResult(
            room_number=structured_output.get("room_number"),
            building_name=structured_output.get("building_name"),
            address=structured_output.get("address"),
            floor_number=structured_output.get("floor_number"),
            accessibility=bool(structured_output.get("accessibility", False)),
        )

        # If there are any attributes extracted by initial_LLM,
        # use internal methods _chromaDB and _verification_LLM
        # to extract any applicable feature types and/or room descriptions
        attributes = structured_output.get("attributes")
        if attributes:
            # Extract candidates (possible attributes) from chromaDB
            candidates = self._chromaDB(attributes)
            if self.debug:
                print("\n2: ChromaDB: Candidates", candidates)

            # Select only applicable attributes from the candidates
            verified_attributes = self._verification_LLM(user_input, candidates)
            if self.debug:
                        print("3: LLM verification:", verified_attributes)

            # Add any verified attributes to the result
            result.feature_type = verified_attributes.get("feature_type")
            result.room_description = verified_attributes.get("room_description")
        else:
            print("No attributes detected.")

        # Return the full QueryResult object
        return result


    # LLM initial layer: Generate a structured output extracted from the user input
    def _initial_LLM(self, user_input):
        return self.llamaLLM.prompt(
            user_input, 
            PROMPT_ENGINEERING_INPUT, 
            RESPONSE_FORMAT_INPUT
        )

    # ChromaDB layer: Find candidates from vector database.
    # Candidates are existing feature types or room descriptions 
    # from the PostGIS database, referred to collectively as 'attributes'.
    def _chromaDB(self, attributes):
        # Search separately in the collection for each given attribute
        response = self.collection.queryResponse(attributes)

        if self.debug:
            # TODO: Remove the TESTING print
            print("\n TESTING: ", response["documents"])
            self._log_chroma_results(attributes, response)

        # Flatten ChromaDB results into one list TODO: Fix wording based on TESTING
        all_results = zip(response["documents"], response["metadatas"])

        # Select candidates: Only first result for each search
        # Each entry is a pair of doc (attribute name) and type (feature/description)
        candidates = []
        for docs, metas in all_results:
            candidates.append((docs[0], metas[0].get("type")))      

        return candidates

    # LLM verification layer: Select attributes that are relevant to the original input
    def _verification_LLM(self, user_input, candidates):
        # Combine the original question with the attribute candidates from chromaDB
        prompt = f'''User: {user_input}, Candidates:{candidates}'''

        return self.llamaLLM.prompt(
            prompt,
            PROMPT_ENGINEERING_VALIDATION,
            RESPONSE_FORMAT_VALIDATION
        )

    # Prints distances for the results in ChromaDB
    @staticmethod
    def _log_chroma_results(attributes, response):
        print("ChromaDB results:")

        for word, documents, metadatas, distances in zip(
            attributes,
            response["documents"],
            response["metadatas"],
            response["distances"],
        ):
            print(f"\nSøgning: {word}")

            for document, metadata, distance in zip(documents, metadatas, distances):
                print(f"{document}, {metadata}: {distance:.4f}")