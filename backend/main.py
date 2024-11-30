import logging
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
    try:
        while True:
            data = await websocket.receive_text()
            logger.info("Human: %s", data)
            parsed_data = json.loads(data)
            logger.info("Parsed data: %s", parsed_data)
            input_value = parsed_data.get("message")
            selected_city = parsed_data.get("city")
            logger.info("selected_city: %s", selected_city)

            # AI Pipeline
            result = run_handler(input_value, vectorstore, selected_city)

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
