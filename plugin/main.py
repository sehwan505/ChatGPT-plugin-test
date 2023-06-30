from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import pinecone_db
from dart import dart_api

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pinecone_db.router)
app.include_router(dart_api.router)
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")