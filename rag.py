import os
from typing import List, Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class SemanticAPIRouter:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        # Use Hugging Face embeddings from LangChain
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)

        # Define API database as documents
        docs = [
            Document(
                page_content='Servizio Tessera a Te: Servizio per assistenza e prenotazione tessere "Dedicata a te".',
                metadata={
                    "api_endpoint": "tessera_api",
                    "service_name": "Tessera a Te",
                },
            ),
            Document(
                page_content="Legalizzazione atti consolari e certificati italiani: Servizio di autenticazione documenti per atti consolari. Date disponibili a richiesta.",
                metadata={
                    "api_endpoint": "consolari_api",
                    "service_name": "Legalizzazione Atti Consolari",
                },
            ),
        ]

        # Create vector store
        self.vectorstore = Chroma.from_documents(docs, self.embeddings)

        # Mock API services
        self.api_services = {
            "tessera_api": self.get_tessera_api_dates,
            "consolari_api": self.get_legalizzazione_atti_api_dates,
        }

        # Initialize language model for final response generation
        self.llm = ChatOpenAI(
            temperature=0,
            model="Meta-Llama-3.1-8B-Instruct",
            openai_api_key=os.getenv("API_KEY"),
            openai_api_base=os.getenv("API_ENDPOINT"),
        )

        # Create prompt template for refining the query
        self.refine_prompt = PromptTemplate(
            input_variables=["query"],
            template="""Given the following user query, refine it to better match a service in the vectorstore. (remove non relevant data):
Query: {query}

Refined Query:""",
        )

        # Create LLM chain for refining the query
        self.refine_chain = LLMChain(llm=self.llm, prompt=self.refine_prompt)

        # Create prompt template for function call generation
        self.function_call_prompt = PromptTemplate(
            input_variables=["query"],
            template="""Given the following user query, determine the best service to call and return the corresponding function call:
Query: {query}

Function Call:""",
        )

        # Create LLM chain for function call generation
        self.function_call_chain = LLMChain(
            llm=self.llm, prompt=self.function_call_prompt
        )

        # Create prompt template for response generation
        self.response_prompt = PromptTemplate(
            input_variables=["query", "service", "dates"],
            template="""Rispondi alla seguente richiesta in modo naturale:
Query originale: {query}
Servizio: {service}
Date disponibili: {dates}

Fornisci una risposta cortese e chiara sulle date disponibili.""",
        )

        # Create LLM chain for response generation
        self.response_chain = LLMChain(llm=self.llm, prompt=self.response_prompt)

    def find_most_similar_service(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Find the most semantically similar services to the given query

        :param query: User's semantic query
        :param k: Number of top results to return
        :return: List of top k similar service documents
        """
        # Perform similarity search
        results = self.vectorstore.similarity_search(query, k=k)

        if not results:
            raise ValueError("No matching service found")

        return results

    def get_tessera_api_dates(self) -> List[str]:
        """
        Mock API for Tessera a Te service

        :return: List of available dates
        """
        return ["4 dicembre", "11 dicembre"]

    def get_legalizzazione_atti_api_dates(self) -> List[str]:
        """
        Mock API for legalizzazione_atti service

        :return: List of available dates
        """
        return ["5 dicembre", "12 dicembre"]

    def process_query(self, query: str) -> str:
        """
        Process the semantic query end-to-end

        :param query: User's semantic query
        :return: Generated response
        """
        try:
            # Refine the user query to better match the services
            refined_query = self.refine_chain.invoke({"query": query})["text"]

            # Determine the best function call to use
            function_call = self.function_call_chain.invoke({"query": refined_query})[
                "text"
            ]

            # Extract the function name from the function call
            function_name = function_call.split("(")[0].strip()

            # Call the corresponding API to get dates
            available_dates = self.api_services[function_name]()

            # Generate natural language response
            response = self.response_chain.invoke(
                {
                    "query": query,
                    "service": function_name,
                    "dates": ", ".join(available_dates),
                }
            )["text"]

            return response

        except Exception as e:
            return f"Mi dispiace, si è verificato un errore: {str(e)}"


def main():
    # Example usage
    router = SemanticAPIRouter()

    # Test queries
    queries = [
        "voglio prenotare la tessera a te, quali giorni ci sono disponibili?",
        # "Vorrei informazioni sulla legalizzazione di atti consolari",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        response = router.process_query(query)
        print("Risposta:", response)


if __name__ == "__main__":
    main()
