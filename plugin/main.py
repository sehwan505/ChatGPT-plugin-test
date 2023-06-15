from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import pinecone_db

app = FastAPI()

origins = [
    "http://http://104.155.157.27/",
    "http://localhost",
    "http://localhost:8000",
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
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")