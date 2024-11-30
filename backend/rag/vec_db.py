import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb import Settings as chroma_settings
from langchain.docstore.document import Document

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chroma_add.log"),
        logging.StreamHandler()
    ]
)

class ChromaDB:
    def __init__(self,docs = None,persist_directory="./chroma_data"):
        
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.setting = chroma_settings(is_persistent=True, anonymized_telemetry=False)
        if docs is None:
            self.vectorstore = Chroma(persist_directory=persist_directory,client_settings=self.setting,embedding_function=self.embeddings)
        else:
            self.vectorstore = Chroma.from_documents(documents=docs,embedding=self.embeddings, persist_directory=persist_directory, client_settings=self.setting)


    # Inizializza il database Chroma
    # Aggiunge informazioni al database vettoriale
    def add_to_chroma(self, documents):
        try:
            logging.info("Aggiunta dei documenti al database Chroma...")
            texts = [doc.content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            # Aggiunge i documenti e i relativi metadati
            self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
            logging.info(f"Aggiunti {len(documents)} documenti a Chroma.")
        except Exception as e:
            logging.error(f"Errore durante l'aggiunta di documenti a Chroma: {e}")
            raise


    def get_from_chroma(vectorstore, query):
        try:
            logging.info("Esecuzione della ricerca su Chroma...")
            results = vectorstore.similarity_search(query, k=1)
            logging.info("Ricerca completata con successo.")
            return results
        except Exception as e:
            logging.error(f"Errore durante l'elaborazione della query: {e}")
            raise



if __name__ == "__main__":
    try:
        # Definizione dei documenti
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

        # Inizializza il vectorstore Chroma
        vector_store = ChromaDB(docs)
        #vector_store.add_to_chroma(docs)

        # Aggiungi i documenti a Chroma
        
    except Exception as e:
        logging.error(f"Errore nell'esecuzione del file: {e}")