from beanie import Document, Indexed
from datetime import datetime
from pydantic import BaseModel
from typing import Annotated, Optional

class ChannelInfo(BaseModel):
  info_date: datetime = datetime.now()
  title: str
  description: str
  custom_url: Optional[str]
  published_at: str
  thumbnails: dict
  default_language: str
  country: str
  view_count: int
  subscriber_count: int
  video_count: int

class Channel(Document):
  channel_id: Annotated[str, Indexed(unique=True)]
  info: Optional[ChannelInfo] = None


# channel_example = {'kind': 'youtube#channel',
#  'etag': 'JUEXK2ETlaO2yaDXbKnp0kN24lI',
#  'id': 'UC7Elc-kLydl-NAV4g204pDQ',
#  'snippet': {'title': 'Популярная политика',
#   'description': '«Популярная политика» — канал, на котором говорят правду о войне, развязанной Путиным против Украины. Присоединяйтесь. Не подчиняйтесь.\n\nДля коммерческих запросов: info@politica.media\n\nНаш телеграм-канал: https://t.me/politica_media\n',
#   'customUrl': '@popularpolitics',
#   'publishedAt': '2017-06-27T14:12:04Z',
#   'thumbnails': {'default': {'url': 'https://yt3.ggpht.com/EvmWYOa6vP10HrtJsdag4X4Lkjxp7fVnB8GyT73d-SBBUJZv-OJYOszeebTW5eZW5glXbtatt7E=s88-c-k-c0x00ffffff-no-rj',
#     'width': 88,
#     'height': 88},
#    'medium': {'url': 'https://yt3.ggpht.com/EvmWYOa6vP10HrtJsdag4X4Lkjxp7fVnB8GyT73d-SBBUJZv-OJYOszeebTW5eZW5glXbtatt7E=s240-c-k-c0x00ffffff-no-rj',
#     'width': 240,
#     'height': 240},
#    'high': {'url': 'https://yt3.ggpht.com/EvmWYOa6vP10HrtJsdag4X4Lkjxp7fVnB8GyT73d-SBBUJZv-OJYOszeebTW5eZW5glXbtatt7E=s800-c-k-c0x00ffffff-no-rj',
#     'width': 800,
#     'height': 800}},
#   'defaultLanguage': 'ru',
#   'localized': {'title': 'Популярная политика',
#    'description': '«Популярная политика» — канал, на котором говорят правду о войне, развязанной Путиным против Украины. Присоединяйтесь. Не подчиняйтесь.\n\nДля коммерческих запросов: info@politica.media\n\nНаш телеграм-канал: https://t.me/politica_media\n'},
#   'country': 'LT'},
#  'statistics': {'viewCount': '1976675604',
#   'subscriberCount': '2740000',
#   'hiddenSubscriberCount': False,
#   'videoCount': '10772'}}