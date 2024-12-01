import logging
import random
from typing import List

import debugpy
from fastapi import FastAPI, WebSocket
from init_db import load_documents_from_directory
from rag.chain import initialize_chroma, run_handler
import json

logger = logging.getLogger(__name__)

# Enable debugger
debugpy.listen(("0.0.0.0", 5678))

app = FastAPI()

# Store active connections
active_connections: List[WebSocket] = []

docs = load_documents_from_directory("./documents")
# Inizializza il vectorstore Chroma
vectorstore = initialize_chroma(docs)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    welcomes = [
        "Ciao, sono PAI! Il tuo assistente per navigare i servizi della pubblica amministrazione. Come posso esserti utile?",
        "Ciao! Sono PAI, il tuo assistente personale per esplorare i servizi della pubblica amministrazione. Come posso aiutarti oggi?",
        "Benvenuto! Sono PAI, il tuo alleato per semplificare l'accesso ai servizi pubblici. Come posso esserti utile?"
    ]
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

    try:
        history = []

        while True:
            data = await websocket.receive_text()
            logger.info("Human: %s", data)
            parsed_data = json.loads(data)
            logger.info("Parsed data: %s", parsed_data)
            input_value = parsed_data.get("message")
            history.append(f"human asked: {input_value}\n")
            selected_city = parsed_data.get("city")
            logger.info("selected_city: %s", selected_city)

            # AI Pipeline
            result = run_handler("".join(history), vectorstore, selected_city)

            history.append(f"you answered: {result}\n")

            while len(history) > 4:
                history.pop(0)

            """
            Broadcast in teoria inutile visto che la comunicazione è 1-1

            # Send back the human message to all clients
            for connection in active_connections:
                await connection.send_json({
                    "sender": "Human",
                    "message": data
                })
            """

            agent_message = result
            print("Agent:", agent_message)

            # Send computer response to all clients
            for connection in active_connections:
                await connection.send_json(
                    {"sender": "Computer", "message": agent_message}
                )

    except:
        active_connections.remove(websocket)
