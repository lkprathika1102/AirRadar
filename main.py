from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database.models import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index():
    return {"status": "AirRadar active"}