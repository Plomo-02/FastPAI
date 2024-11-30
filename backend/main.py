import logging
from typing import List

import debugpy
from fastapi import FastAPI, WebSocket
from init_db import load_documents_from_directory
from rag.chain import initialize_chroma, run_handler

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

            # AI Pipeline
            result = run_handler(data, vectorstore, "napoli")

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
