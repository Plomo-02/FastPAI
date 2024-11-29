from langchain.prompts import PromptTemplate
import os
from langchain.chains.base import Chain
import logging
from rag.vec_db import ChromaDB
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chain_app.log"),
        logging.StreamHandler()
    ]
)

# Configura Llama 3.1


# Configura il prompt per la formattazione della query
def create_prompt():
    template = """
    Prendi questa richiesta dell'utente e formattala per una query vettoriale:
    {input_text}
    """
    return PromptTemplate(input_variables=["input_text"], template=template)

# Configura il vectorstore Chroma
def initialize_chroma():
    db = ChromaDB()
    return db.vectorstore

# Crea una chain personalizzata
class LlamaChromaChain(Chain):
    def __init__(self, vectorstore):
        super().__init__()
        self.llm = ChatOpenAI(
            temperature=0,
            model="Meta-Llama-3.1-8B-Instruct",
            openai_api_key=os.getenv("API_KEY"),
            openai_api_base=os.getenv("API_ENDPOINT"),
        )
        
        self.vectorstore = vectorstore

    def _call(self, inputs: dict) -> dict:
        query = inputs["input_text"]

        # Fase 1: Formatta la query con Llama
        logging.info("Formattazione della query con Llama...")
        formatted_query = self.llm(f"Formatta questa richiesta per una query vettoriale: {query}")
        formatted_query = formatted_query.strip()

        # Fase 2: Ricerca nel vectorstore
        logging.info("Esecuzione della ricerca su Chroma...")
        results = self.vectorstore.similarity_search(formatted_query, k=3)

        # Restituisci i risultati
        return {"results": results}

    @property
    def input_keys(self):
        return ["input_text"]

    @property
    def output_keys(self):
        return ["results"]

# Funzione principale per eseguire la chain
def run_chain(query: str):
    try:
       
        logging.info("Avvio della catena LangChain...")
        
        # Inizializza Llama e Chroma
        vectorstore = initialize_chroma()
        

        # Crea la catena
        chain = LlamaChromaChain(vectorstore=vectorstore)

        # Esegui la catena con la query
        result = chain.run({"input_text": query})

        # Mostra i risultati
        logging.info("Risultati della catena:")
        for item in result["results"]:
            logging.info(f" - Contenuto: {item['content']}")
            logging.info(f" - Metadata: {item['metadata']}")
    except Exception as e:
        logging.error(f"Errore durante l'esecuzione della catena: {e}")
        raise
