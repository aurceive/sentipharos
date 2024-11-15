from beanie import Document, Indexed
from datetime import datetime
from pydantic import BaseModel
from typing import Annotated, Optional

from .video import Video

# class Embedding(BaseModel):
#   model: str
#   embedding: list[float]

class Comment(Document):
  comment_id: Annotated[str, Indexed(unique=True)]
  video: Video
  text_display: str
  text_original: str
  author_display_name: str
  author_profile_image_url: Optional[str]
  author_channel_url: Optional[str]
  author_channel_id: Optional[str]
  like_count: int
  published_at: Annotated[str, Indexed()]
  updated_at: str
  embedding: Annotated[Optional[list[float]], Indexed(partialFilterExpression={"embedding": None})] = None

# comment_example = {
#   'kind': 'youtube#commentThread',
#   'etag': 'Vj0XuSuCPMgMEAk3J6m_GuSDrcw',
#   'id': 'UgyCEJzU_3BHuQkINS14AaABAg',
#   'snippet': {
#     'channelId': 'UC7Elc-kLydl-NAV4g204pDQ',
#     'videoId': 'fPr3vbxnNew',
#     'topLevelComment': {
#       'kind': 'youtube#comment',
#       'etag': 'mYfjUxquZo1cQmy3IALFH0yEn7o',
#       'id': 'UgyCEJzU_3BHuQkINS14AaABAg',
#       'snippet': {
#         'channelId': 'UC7Elc-kLydl-NAV4g204pDQ',
#         'videoId': 'fPr3vbxnNew',
#         'textDisplay': 'Почему Кац только сейчас выступил с &quot;расследованием&quot;?<br>Заказ был сделан давно, но тяжёлая работа с документами - это не для Каца. Отделывался короткими нападками на ФБК.<br>Но, как только увидел обложку книги Навального, с криком: &quot;На его месте должен быть я!&quot;, застрочил как бешенный принтер.<br>И до сих пор не может успокоиться',
#         'textOriginal': 'Почему Кац только сейчас выступил с "расследованием"?\nЗаказ был сделан давно, но тяжёлая работа с документами - это не для Каца. Отделывался короткими нападками на ФБК.\nНо, как только увидел обложку книги Навального, с криком: "На его месте должен быть я!", застрочил как бешенный принтер.\nИ до сих пор не может успокоиться',
#         'authorDisplayName': '@sercher8531',
#         'authorProfileImageUrl': 'https://yt3.ggpht.com/ytc/AIdro_l9XlnQS1N86VJcx6PPKCocfYnuU7sgnYwJNZU7Wu7XWiQ=s48-c-k-c0x00ffffff-no-rj',
#         'authorChannelUrl': 'http://www.youtube.com/@sercher8531',
#         'authorChannelId': {'value': 'UCZ1urtzPDhx_B_OcpW1KLiQ'},
#         'canRate': True,
#         'viewerRating': 'none',
#         'likeCount': 0,
#         'publishedAt': '2024-10-31T18:46:44Z',
#         'updatedAt': '2024-10-31T18:46:44Z'
#       }
#     },
#     'canReply': True,
#     'totalReplyCount': 0,
#     'isPublic': True
#   }
# }
