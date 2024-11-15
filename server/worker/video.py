# Данный воркер должен делать следующее:
# 1. Доставать все коментарии из под видео, на которые есть подписка и сохранять их в базу данных
# 2. Периодически проверять наличие новых комментариев

import asyncio
import logging
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from server.db.video import Video
from server.db.comment import Comment
import os
from typing import List, Optional
from googleapiclient.discovery import build


API_KEY = os.getenv("YOUTUBE_API_KEY", 'AIzaSyDmeT8Isv-2I-jkqr5K5o8bEhXg66JfTEQ') # TODO: secure this token
mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://admin:admin@sentipharos.nnvrgyb.mongodb.net/?retryWrites=true&w=majority&appName=Sentipharos") # TODO: secure this uri
client = AsyncIOMotorClient(mongo_uri)
youtube = build('youtube', 'v3', developerKey=API_KEY)

async def get_subscribed_videos():
  videos = await Video.find(Video.subscription == True).to_list()
  return videos

async def get_comments(video_id: str, page_token: Optional[str] = None) -> tuple[Optional[List[dict]], Optional[str]]:
  comments = []
  request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    order="time",
    pageToken=page_token,
    maxResults=100
  )
  try:
    response = request.execute()
    for item in response['items']:
      comment = item['snippet']['topLevelComment']
      comments.append(comment)
    return comments, response.get('nextPageToken')
  except Exception as e:
    logging.error(f"Error getting comments for video {video_id}: {e}")
    return None, None

async def save_comments(comments: List[dict], video: Video) -> bool:
  exist = False
  for comment in comments:
    try:
      snippet = comment['snippet']
      existing_comment = await Comment.find_one(Comment.comment_id == comment['id'])
      if not existing_comment:
        new_comment = Comment(
          comment_id=comment['id'],
          video=video,
          text_display=snippet['textDisplay'],
          text_original=snippet['textOriginal'],
          author_display_name=snippet['authorDisplayName'],
          author_profile_image_url=snippet['authorProfileImageUrl'],
          author_channel_url=snippet['authorChannelUrl'],
          author_channel_id=snippet['authorChannelId']['value'],
          like_count=snippet['likeCount'],
          published_at=snippet['publishedAt'],
          updated_at=snippet['updatedAt']
        )
        await new_comment.insert()
      else:
        exist = True
    except Exception as e:
      logging.error(f"Error saving comment {comment.get('id', 'unknown')}: {e}")
  if not exist:
    logging.info(f"Saved {len(comments)} comments for video {video.video_id}")
  return exist

async def process_video(video: Video):
  page_token = None
  while True:
    comments, page_token = await get_comments(video.video_id, page_token)
    if comments:
      exist = await save_comments(comments, video)
      if exist and video.first_comment_fetched:
        break
      if not page_token:
        video.first_comment_fetched = True
        await video.save()
        break
    else:
      break
    await asyncio.sleep(1)

async def main():
  await init_beanie(database=client.get_database("sentipharos"), document_models=[Video, Comment])
  
  if not await Video.find_one(Video.video_id == "hjVe7WztrdY"):
    await Video(video_id="hjVe7WztrdY", subscription=True).insert()

  while True:
    videos = await get_subscribed_videos()
    for video in videos:
      await process_video(video)
    await asyncio.sleep(60 * 10)

if __name__ == "__main__":
  asyncio.run(main())
