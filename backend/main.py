import logging
import random
from typing import List, Dict
import debugpy
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from init_db import load_documents_from_directory
from rag.chain import initialize_chroma, run_handler
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Enable debugger
debugpy.listen(("0.0.0.0", 5678))

app = FastAPI()

# Load documents and initialize vector store
docs = load_documents_from_directory("./documents")
vectorstore = initialize_chroma(docs)


# Manages per-user session state
class WebSocketConnectionManager:
    def __init__(self):
        # Dictionary to store active connections and their session histories
        self.active_connections: Dict[str, Dict] = {}

    async def connect(self, websocket: WebSocket):
        """
        Establish a new WebSocket connection and initialize its session

        Args:
            websocket (WebSocket): The incoming WebSocket connection

        Returns:
            str: A unique session identifier for this connection
        """
        await websocket.accept()

        # Generate a unique session ID
        # You might want to use a more robust method in production
        session_id = str(id(websocket))

        # Initialize session state
        self.active_connections[session_id] = {"websocket": websocket, "history": []}

        return session_id

    def disconnect(self, session_id: str):
        """
        Remove a WebSocket connection from active connections

        Args:
            session_id (str): The unique identifier for the session
        """
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_welcome_message(self, session_id: str):
        """
        Send a welcome message to a specific WebSocket connection

        Args:
            session_id (str): The unique identifier for the session
        """
        welcomes = [
            "Ciao, sono PAI! Il tuo assistente per navigare i servizi della pubblica amministrazione. Come posso esserti utile?",
            "Ciao! Sono PAI, il tuo assistente personale per esplorare i servizi della pubblica amministrazione. Come posso aiutarti oggi?",
            "Benvenuto! Sono PAI, il tuo alleato per semplificare l'accesso ai servizi pubblici. Come posso esserti utile?",
        ]

        websocket = self.active_connections[session_id]["websocket"]
        await websocket.send_json(
            {
                "message": {
                    "llm_response": {
                        "info": random.choice(welcomes),
                        "is_info": True,
                    },
                    "response": [],
                    "info": "",
                }
            }
        )

    async def handle_message(self, session_id: str, data: str):
        """
        Process an incoming message for a specific session

        Args:
            session_id (str): The unique identifier for the session
            data (str): The incoming message data
        """
        session = self.active_connections[session_id]
        websocket = session["websocket"]
        history = session["history"]

        try:
            # Parse the incoming message
            parsed_data = json.loads(data)
            logger.info(f"Session {session_id} - Parsed data: {parsed_data}")

            input_value = parsed_data.get("message")
            selected_city = parsed_data.get("city")

            # Add human input to history
            history.append(f"human asked: {input_value}\n")

            # Run the RAG pipeline
            result = run_handler("".join(history), vectorstore, selected_city)

            # Add AI response to history
            history.append(f"you answered: {result}\n")

            # Maintain a limited history (last 4 exchanges)
            while len(history) > 4:
                history.pop(0)

            # Send response back to the client
            await websocket.send_json({"sender": "Computer", "message": result})

        except Exception as e:
            logger.error(f"Error in session {session_id}: {e}")
            # Optionally send an error message back to the client
            await websocket.send_json(
                {
                    "sender": "System",
                    "message": "An error occurred while processing your request.",
                }
            )


# Create a connection manager instance
connection_manager = WebSocketConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint that handles individual user connections
    """
    session_id = None
    try:
        # Establish connection and get session ID
        session_id = await connection_manager.connect(websocket)

        # Send welcome message
        await connection_manager.send_welcome_message(session_id)

        # Listen for messages
        while True:
            data = await websocket.receive_text()
            logger.info(f"Session {session_id} - Received: {data}")

            # Handle the incoming message
            await connection_manager.handle_message(session_id, data)

    except WebSocketDisconnect:
        logger.info(f"WebSocket {session_id} disconnected")
        if session_id:
            connection_manager.disconnect(session_id)

    except Exception as e:
        logger.error(f"Unexpected error in WebSocket {session_id}: {e}")
        if session_id:
            connection_manager.disconnect(session_id)


# Optional: Add a health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
