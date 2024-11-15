# Данный воркер должен делать следующее:
# 1. Для комментариев, у которых ещё нет эмбеддинга, делать запрос к сервису и сохранять эмбеддинги в базу данных

import asyncio
import logging
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from server.db.video import Video
from server.db.comment import Comment
import os
import requests

FES_API_URL = "https://fes-qrrel3xmdq-lz.a.run.app/predict" # TODO: secure this url
mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://admin:admin@sentipharos.nnvrgyb.mongodb.net/?retryWrites=true&w=majority&appName=Sentipharos") # TODO: secure this uri
client = AsyncIOMotorClient(mongo_uri)
comments_in_progress: set[str] = set()
stop = False

class FESRequest(BaseModel):
  inputs: list[str]

class FESResponse(BaseModel):
  model: str
  outputs: list[list[float]]


async def get_comments_from_db():
  global stop
  # Если комментариев на обновление < 100, то лучше пока не обновлять, чтобы лишний раз не поднимать fes
  if stop and (
    await Comment.aggregate([{ "$match": { "embedding": None } }, { "$count": "count" }]).to_list(length=1)
  )[0].get("count", 0) < 100:
    return []
  comments = await Comment.find(Comment.embedding == None, {"_id": {"$nin": comments_in_progress}}, limit=10).to_list()
  comments_in_progress.update(str(comment.id) for comment in comments)
  stop = len(comments) < 1 and len(comments_in_progress) < 1
  return comments

async def get_embedding(request: FESRequest) -> FESResponse:
  response = requests.post(FES_API_URL, json={"inputs": request.inputs})
  if response.status_code == 200:
    fes_response = FESResponse(**response.json())
    return fes_response
  else:
    raise Exception(f"Error getting embedding: {response.status_code} - {response.text}")

async def update_comments_embedding(comments: list[Comment]):
  fes_request = FESRequest(inputs=[comment.text_original for comment in comments])
  try:
    fes_response = await get_embedding(fes_request)
    for i, comment in enumerate(comments):
      try:
        comment.embedding = fes_response.outputs[i]
        await comment.save()
      except Exception as e:
        logging.error(f"Error saving comment: {e}")
        comment.embedding = None
        await comment.save()
    
    logging.info(f"Updated {len(comments)} comments")
    print(f"Updated {len(comments)} comments")
  except Exception as e:
    logging.error(f"Error updating embeddings: {e}")
  finally:
    comments_in_progress.difference_update(str(comment.id) for comment in comments)

async def main():
  await init_beanie(database=client.get_database("sentipharos"), document_models=[Video, Comment])
  
  while True:
    comments = await get_comments_from_db()
    if len(comments) > 0:
      if len(comments_in_progress) > 100:
        await asyncio.sleep(1)
        continue
      await update_comments_embedding(comments)
    else:
      await asyncio.sleep(60 * 5)

if __name__ == "__main__":
  asyncio.run(main())
