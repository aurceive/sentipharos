from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from server.common import FES_API_URL, MONGO_URI, logger
from server.db.youtube.video import Video
from server.db.youtube.comment import Comment
import aiohttp, asyncio

client = AsyncIOMotorClient(MONGO_URI)
comments_to_process: list[Comment] = []
comments_in_process: list[Comment] = []
fes_requests_in_process: int = 0
max_fes_requests = 10
batch_size = 1
stop = False
comments_updated = 0

class FESRequest(BaseModel):
  inputs: list[str]

class FESResponse(BaseModel):
  model: str
  outputs: list[list[float]]


async def get_comments_from_db():
  global stop
  # Если комментариев на обновление < 100, то лучше пока не обновлять, чтобы лишний раз не поднимать fes
  if stop and (
    await Comment.aggregate([{"$match": {"embedding": None}}, {"$count": "count"}]).to_list(length=1)
  )[0].get("count", 0) < 100:
    return
  
  comments = await Comment.find(
    Comment.embedding == None, {"_id": {"$nin": [str(comment.id) for comment in comments_in_process + comments_to_process]}},
    limit=100
  ).to_list()
  comments_to_process.extend(comments)
  stop = len(comments_to_process) < 1 and len(comments_in_process) < 1

async def get_embedding(session: aiohttp.ClientSession, request: FESRequest) -> FESResponse:
  """Отправляет асинхронный запрос на FES API для получения встраивания"""
  async with session.post(FES_API_URL, json=request.model_dump()) as response:
    if response.status == 200:
      fes_response = FESResponse(**await response.json())
      return fes_response
    else:
      error_text = await response.text()
      raise Exception(f"Error getting embedding: {response.status} - {error_text}")

async def update_comments_embedding(session: aiohttp.ClientSession, comments: list[Comment]):
  """Обновляет встраивание комментариев, отправляя их текст на FES API"""
  texts = [comment.info.text_original for comment in comments]
  fes_request = FESRequest(inputs=texts)
  try:
    fes_response = await get_embedding(session, fes_request)
  except Exception as e:
    logger.error(f"Error getting embeddings: {e}")
    for comment in comments:
      comments_in_process.remove(comment)
      comments_to_process.append(comment)
    return
  finally:
    global fes_requests_in_process
    fes_requests_in_process -= 1
  for comment, embedding in zip(comments, fes_response.outputs):
    try:
      comment.embedding = embedding
      await comment.save()
      global comments_updated
      comments_updated += 1
    except Exception as e:
      logger.error(f"Error updating embedding: {e}")
      comment.embedding = None
      await comment.save()
      comments.remove(comment)
    finally:
      comments_in_process.remove(comment)
  if comments_updated >= 100:
    logger.info(f"Updated {comments_updated} comments")
    comments_updated = 0

async def comments_worker(session: aiohttp.ClientSession, toggle: list[bool]):
  global fes_requests_in_process
  while toggle[0]:
    if not comments_to_process:
      await asyncio.sleep(10)
      continue
    if fes_requests_in_process < max_fes_requests:
      fes_requests_in_process += 1
      _batch_size = min(batch_size, len(comments_to_process))
      comments_batch = [comments_to_process.pop() for _ in range(_batch_size)]
      comments_in_process.extend(comments_batch)
      asyncio.create_task(update_comments_embedding(session, comments_batch))
      continue
    await asyncio.sleep(1)

async def bd_worker(toogle: list[bool]):
  while toogle[0]:
    if len(comments_to_process) > 100:
      await asyncio.sleep(1)
      continue
    await get_comments_from_db()
    if stop:
      await asyncio.sleep(60 * 5)

async def main(toogle: list[bool]):
  # Инициализация базы данных
  await init_beanie(database=client.get_database("sentipharos"), document_models=[Video, Comment])

  logger.info("Comment worker started")
  
  # Открываем асинхронную сессию
  async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(3600)) as session:
    await asyncio.gather(comments_worker(session, toogle), bd_worker(toogle))

if __name__ == "__main__":
  toogle = [True]
  asyncio.run(main(toogle))
