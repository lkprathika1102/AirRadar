import asyncio
import os
import sys
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from database.models import init_db
from core.scanner import BLEManager
from typing import List

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

async def scanner_callback(payload):
    await manager.broadcast(payload)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    scanner = BLEManager(scanner_callback)
    scan_task = asyncio.create_task(scanner.start_scan())
    yield
    await scanner.stop_scan()
    scan_task.cancel()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=get_resource_path("static")), name="static")

@app.get("/")
async def index():
    return RedirectResponse(url="/static/index.html")

@app.websocket("/ws/radar")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
