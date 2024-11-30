import json
import logging
import os

from chromadb import Settings as chroma_settings
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("chroma_add.log"), logging.StreamHandler()],
)


class ChromaDB:
    def __init__(self, docs=None, persist_directory="./chroma_data"):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.setting = chroma_settings(is_persistent=True, anonymized_telemetry=False)
        if docs is None:
            self.vectorstore = Chroma(
                persist_directory=persist_directory,
                client_settings=self.setting,
                embedding_function=self.embeddings,
            )
        else:
            self.vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=self.embeddings,
                persist_directory=persist_directory,
                client_settings=self.setting,
            )

    def add_to_chroma(self, documents):
        try:
            logging.info("Aggiunta dei documenti al database Chroma...")
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]

            # Aggiunge i documenti e i relativi metadati
            self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
            logging.info(f"Aggiunti {len(documents)} documenti a Chroma.")
        except Exception as e:
            logging.error(f"Errore durante l'aggiunta di documenti a Chroma: {e}")
            raise

    def get_from_chroma(self, query, comune="roma"):
        try:
            logging.info("Esecuzione della ricerca su Chroma...")
            results = self.vectorstore.similarity_search(
                query, k=1, filter={"comune": comune}
            )
            logging.info("Ricerca completata con successo.")
            return results
        except Exception as e:
            logging.error(f"Errore durante l'elaborazione della query: {e}")
            raise




