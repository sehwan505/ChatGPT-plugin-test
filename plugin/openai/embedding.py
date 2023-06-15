import requests, json
import openai
from fastapi import APIRouter
from util import config

openai.api_key = config["OPENAI_KEY"]

router = APIRouter(
    prefix="/api",
)

def get_embedding(text):
    """
    Get the embedding for a given text
    """
    results = openai.Embedding.create(input=text, model="text-embedding-ada-002")

    return results["data"][0]["embedding"]