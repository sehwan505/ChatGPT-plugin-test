import openai
import pinecone
from util import config
from fastapi import APIRouter
import uuid
from typing import List
from pydantic import BaseModel

class Text(BaseModel):
    content: str

openai.api_key = config["OPENAI_KEY"]
PINECONE_API_KEY = config["PINECONE_KEY"]
PINECONE_API_ENV = config["PINECONE_ENV"]

router = APIRouter(
    prefix="/db",
)

@router.get("/get_vector")
def get_vector(embed: List[int]):
    index_name = 'gpt-answers-index'
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)

    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=1536, metric='dotproduct')

    index = pinecone.Index(index_name)
    response = index.query(query_embeds, top_k=5, include_metadata=True, namespace='langchain-namespace')
    return response

@router.post("/add_vector")
def add_vector(text: Text):
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
    index = pinecone.Index('gpt-answers-index')
    
    vectors = [{
                "id": str(uuid.uuid4()),
                "values":get_openai_embedding(text.content),
                "metadata":{'text': text.content}
            }]
    
    upsert_response = index.upsert(
        vectors=vectors,
        namespace='langchain-namespace'
    )

def get_openai_embedding(text: str):
    embed_model = "text-embedding-ada-002"
    embed = openai.Embedding.create(
        input=text,
        engine=embed_model
    )
    embeds = embed['data'][0]['embedding']

    if embeds:
        return embeds
    else:
        raise Exception("Request failed with status code: there is no embeds")