from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from server.db.video import Video
import os
import asyncio

mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://admin:admin@sentipharos.nnvrgyb.mongodb.net/?retryWrites=true&w=majority&appName=Sentipharos")
client = AsyncIOMotorClient(mongo_uri)

async def main():
    await init_beanie(database=client.get_database("sentipharos"), document_models=[Video])
    video_id = "TENQ3vMUG00"
    video = await Video.find_one(Video.video_id == video_id)
    if not video:
        await Video(video_id=video_id, subscription=True).insert()

if __name__ == "__main__":
    asyncio.run(main())

# python -m tests.add_video_to_sub
