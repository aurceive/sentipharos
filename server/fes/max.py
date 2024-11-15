from sentence_transformers import SentenceTransformer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

os.environ['HF_HOME'] = '/root/.cache/huggingface'
model_name = 'intfloat/e5-mistral-7b-instruct'
# model_name = 'intfloat/multilingual-e5-large-instruct'
model = SentenceTransformer(model_name)

# Определим модель данных для запроса и ответа
class Request(BaseModel):
  inputs: str | list[str]

class Response(BaseModel):
  model: str
  outputs: list[float] | list[list[float]]


@app.get("/")
async def root():
  return 'Feature extraction service is running.'

@app.post("/predict")
async def predict(request: Request):

  if not request.inputs:
    raise HTTPException(status_code=400, detail="No inputs provided")
  
  embeddings = model.encode(request.inputs, normalize_embeddings=True)
  
  response = Response(model=model_name, outputs=embeddings.tolist())
  
  return response.model_dump()
