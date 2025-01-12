from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from server.db.youtube.video import Video
from server.db.processes.comment_fetching import CommentSubscription
import os
import asyncio

mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://admin:admin@sentipharos.nnvrgyb.mongodb.net/?retryWrites=true&w=majority&appName=Sentipharos")
client = AsyncIOMotorClient(mongo_uri)

async def main():
  await init_beanie(database=client.get_database("sentipharos"), document_models=[Video])
  video_id = "TENQ3vMUG00"
  video = await Video.find_one(Video.video_id == video_id)
  if not video:
    video = Video(video_id=video_id)
    await video.insert()
  
  subscription = CommentSubscription.find_one(CommentSubscription.video == video)
  if not subscription:
    subscription = CommentSubscription(video=video)
    await subscription.insert()

if __name__ == "__main__":
  asyncio.run(main())

# python -m tests.add_video_to_sub
