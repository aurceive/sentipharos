from time import monotonic
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from server.common import MONGO_URI, YOUTUBE_API_KEY, logger
from server.db.youtube.comment import Comment, CommentInfo
from server.db.youtube.video import Video
from server.db.processes.comment_fetching import CommentSubscription
from typing import Optional
import aiohttp, asyncio

client = AsyncIOMotorClient(MONGO_URI)

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"

async def get_subscriptions() -> list[CommentSubscription]:
  '''Получить все подписки на комментарии'''
  return await CommentSubscription.find().to_list()

async def get_comments(
    session: aiohttp.ClientSession,
    video_id: str,
    page_token: Optional[str] = None,
    limit: int = 100
  ) -> tuple[Optional[list[dict]], Optional[str]]:
  '''Получить комментарии из под видео'''
  comments = []
  url = f'{YOUTUBE_API_BASE}/commentThreads'
  params = {
    'part': 'snippet',
    'videoId': video_id,
    'order': 'time',
    'maxResults': limit,
    'key': YOUTUBE_API_KEY,
    'fields':
      'nextPageToken,items(snippet(topLevelComment(id,\
      snippet(authorDisplayName,authorProfileImageUrl,authorChannelUrl,\
      authorChannelId(value),textDisplay,textOriginal,likeCount,publishedAt,\
      updatedAt))))'
  }

  if page_token:
    params['pageToken'] = page_token

  try:
    async with session.get(url, params=params) as response:
      if response.status != 200:
        logger.error(f'Error fetching comments for video {video_id}: {response.status} - {await response.text()}')
        return None, None
      data = await response.json()
      for item in data.get('items', []):
        comment = item['snippet']['topLevelComment']
        comments.append(comment)
      return comments, data.get('nextPageToken')
  except Exception as e:
    logger.error(f'Error fetching comments for video {video_id}: {e}')
    return None, None


async def save_comments(comments: list[dict], video: Video) -> bool:
  '''Сохраняет комментарии в базе данных, возвращает True, если хотя бы один комментарий уже существует'''
  existing_comment_ids = set()
  if comments:
    existing_comments = await Comment.find({"comment_id": {"$in": [comment['id'] for comment in comments]}}).to_list()
    existing_comment_ids = {comment.comment_id for comment in existing_comments}
  
  new_comments: list[Comment] = []
  for comment in comments:
    try:
      if comment['id'] in existing_comment_ids:
        continue
      snippet = comment['snippet']
      new_comments.append(Comment(
        comment_id=comment['id'],
        video=video,
        info=CommentInfo(
          text_display=snippet['textDisplay'],
          text_original=snippet['textOriginal'],
          author_display_name=snippet['authorDisplayName'],
          author_profile_image_url=snippet.get('authorProfileImageUrl'),
          author_channel_url=snippet.get('authorChannelUrl'),
          author_channel_id=snippet.get('authorChannelId', {}).get('value'),
          like_count=snippet['likeCount'],
          published_at=snippet['publishedAt'],
          updated_at=snippet['updatedAt']
        )
      ))
    except Exception as e:
      logger.error(f'Error saving comment {comment.get("id", "unknown")}: {e}')

  if new_comments:
    try:
      await Comment.insert_many(new_comments)
    except Exception as e:
      logger.error(f'Error saving comments: {e}')
      return False
    logger.info(f'Saved {len(new_comments)} comments for video {video.video_id}')
  # logger.info(f'Query for {video.video_id} returned {len(new_comments)} new comments and {len(existing_comment_ids)} existing comments')
  return len(existing_comment_ids) > 0


async def process_subscription(session: aiohttp.ClientSession, subscription: CommentSubscription):
  '''Обрабатывает комментарии для одного видео'''
  video = subscription.video
  page_token = None
  limit = 10
  while True:
    comments, page_token = await get_comments(session, video.video_id, page_token, limit)
    limit = 100
    if comments:
      exist = await save_comments(comments, video)
      if exist and subscription.first_comment_fetched:
        break
      if not page_token:
        subscription.first_comment_fetched = True
        await subscription.save()
        break
    else:
      break
    await asyncio.sleep(1)

async def main(toggle: list[bool]):
  # Инициализация базы данных
  await init_beanie(database=client.get_database('sentipharos'), document_models=[Comment, CommentSubscription])

  # Создаём тестовую запись, если её ещё нет
  # if not await Video.find_one(Video.video_id == 'hjVe7WztrdY'):
  #   await Video(video_id='hjVe7WztrdY', subscription=True).insert()
  
  logger.info('Video worker started')

  # Открываем асинхронную сессию
  async with aiohttp.ClientSession() as session:
    while toggle[0]:
      start_time = monotonic()
      subscriptions = await get_subscriptions()
      tasks = [process_subscription(session, subscription) for subscription in subscriptions]
      await asyncio.gather(*tasks)
      elapsed_time = monotonic() - start_time
      await asyncio.sleep(60 * 5 - elapsed_time)

if __name__ == '__main__':
  asyncio.run(main([True]))
