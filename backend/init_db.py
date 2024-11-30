import logging
import os
import json
from langchain.schema import Document
from rag.vec_db import ChromaDB

def load_documents_from_directory(directory):
    """
    Load documents from JSON files in the specified directory.

    Expected JSON file structure:
    {
        "content": "Document text content",
        "metadata": {
            "comune": "RM",
            "date-orari": "...",
            "info": "..."
        }
    }
    """
    documents = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        doc_data = json.load(file)

                        # Create a Document object
                        doc = Document(
                            page_content=doc_data.get("page_content", ""),
                            metadata=doc_data.get("metadata", {}),
                        )
                        documents.append(doc)
                        logging.info(f"Loaded document from {filename}")
                except json.JSONDecodeError:
                    logging.error(f"Error decoding JSON from {filename}")
                except Exception as e:
                    logging.error(f"Error processing {filename}: {e}")
    except Exception as e:
        logging.error(f"Error reading directory {directory}: {e}")

    return documents

def main():
    try:
        # Directory containing JSON documents
        document_directory = "./documents"

        # Load documents from the directory
        docs = load_documents_from_directory(document_directory)

        if not docs:
            logging.warning("No documents found in the directory.")
            return

        # Initialize the Chroma vector store with loaded documents
        vector_store = ChromaDB(docs)

        # Example query
        query = "voglio fare il passaporto come posso fare"
        results = vector_store.get_from_chroma(query, comune="BA")

        print("Search Results:")
        for result in results:
            print(f"Content: {result.page_content}")
            print(f"Metadata: {result.metadata}")
            print("---")

    except Exception as e:
        logging.error(f"Errore nell'esecuzione del programma: {e}")


if __name__ == "__main__":
    main()