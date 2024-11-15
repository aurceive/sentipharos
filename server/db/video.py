from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from .channel import Channel

class VideoInfo(BaseModel):
  info_date: datetime = datetime.now()
  published_at: Annotated[str, Indexed()]
  channel: Channel
  title: str
  description: str
  thumbnail_url: str
  channel_title: str
  tags: list[str]
  category_id: str
  view_count: int
  like_count: int
  favorite_count: int
  comment_count: int

class Video(Document):
  video_id: Annotated[str, Indexed(unique=True)]
  info: Optional[VideoInfo] = None
  subscription: bool = False
  first_comment_fetched: bool = False


# video_example = {'kind': 'youtube#video',
#  'etag': 'wqlE8DZCrlwb5sPOIvtV6O8Iyt8',
#  'id': 'fPr3vbxnNew',
#  'snippet': {'publishedAt': '2024-10-29T11:30:20Z',
#   'channelId': 'UC7Elc-kLydl-NAV4g204pDQ',
#   'title': 'Фишман про ответ ФБК Кацу',
#   'description': '«Если Максим Кац заботился о своей репутации, то она потерпела довольно серьёзный ущерб». \n\nГость: \nМихаил Фишман — https://www.instagram.com/fishmanmish \n\nВедущая: \nНино Росебашвили — @ninorosebashvili  \n\nСмотрите полный выпуск по ссылке: https://youtube.com/live/zHIAXdIqxKc \n\n💳 Стать патроном любимой передачи: https://www.patreon.com/Popularpolitics \n💰 Спонсировать канал на YouTube: https://www.youtube.com/c/Popularpolitics/join \n💸 Поддержать нас криптовалютой: https://donate.fbk.info/#crypto \n💶 Все способы поддержки в одном месте: https://donate.fbk.info \n\n📖 Заказать книгу Алексея Навального «Патриот»: https://patriot.navalny.com \n\nВажные ссылки: \n🔹 Оформите пожертвование в поддержку политзаключенных: https://june12.io \n🔹 Бот «Напиши политзеку»: https://t.me/politzekam_bot \n🔹 Штабы Навального. Защищенная платформа для активистов в России: https://shtab.navalny.com \n🔹 Наш проект «Цены сегодня». Отслеживаем рост цен в магазинах с начала войны: https://pricing.day \n🔹 Бот-предложка команды Навального: https://t.me/teamnavalny_bot \n\nПоддержите нашу работу! \n🔸 Нажмите кнопку «Спасибо» под этим видео, чтобы поддержать команду за кадром! \n🔸 Поддерживайте Штабы Навального: https://www.patreon.com/shtab_navalny \n🔸 Покупайте мерч Команды Навального: https://navalny.shop \n\nПодписывайтесь, чтобы узнавать о главном раньше других: \n➖ Телеграм: https://t.me/politica_media \n➖ Инстаграм: https://instagram.com/politica_media \n➖ Твиттер (X): https://twitter.com/politica_media \n➖ Помощь юристов и ответы на главные вопросы о мобилизации в телеграм-канале: https://t.me/mobilizationnews \n➖ Новости без цензуры: телеграм-канал «Сирена»: https://t.me/news_sirena \n➖ YouTube-канал «Самое важное» с Иваном Ждановым, где вас ждёт лучшая аналитика событий недели: https://www.youtube.com/@samoe_vazhnoe \n\n#популярнаяполитика #кац #фишман',
#   'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/fPr3vbxnNew/default.jpg',
#     'width': 120,
#     'height': 90},
#    'medium': {'url': 'https://i.ytimg.com/vi/fPr3vbxnNew/mqdefault.jpg',
#     'width': 320,
#     'height': 180},
#    'high': {'url': 'https://i.ytimg.com/vi/fPr3vbxnNew/hqdefault.jpg',
#     'width': 480,
#     'height': 360},
#    'standard': {'url': 'https://i.ytimg.com/vi/fPr3vbxnNew/sddefault.jpg',
#     'width': 640,
#     'height': 480},
#    'maxres': {'url': 'https://i.ytimg.com/vi/fPr3vbxnNew/maxresdefault.jpg',
#     'width': 1280,
#     'height': 720}},
#   'channelTitle': 'Популярная политика',
#   'tags': ['война',
#    'спецоперация',
#    'популярная политика последнее',
#    'Фишман',
#    'Михаил Фишман',
#    'Фишман интервью',
#    'Фишман про Каца',
#    'Интервью с Фишманом',
#    'Интервью с Михаилом Фишманом',
#    'Ответ фбк',
#    'Кац',
#    'Казначей',
#    'Фишман Кац',
#    'Фишман про Максима Каца',
#    'Ответ Кацу',
#    'Фишман про ответ Кацу',
#    'Фишман про расследование',
#    'Фишман Казначей',
#    'Репутация Каца',
#    'Михаил Фишман про Максима Каца',
#    'Фишман про фильм',
#    'Фишман ФБК',
#    'Навальный',
#    'Навальная',
#    'ФБК',
#    'Команда Навального',
#    'Популярная политика',
#    'Популярная политика последнее'],
#   'categoryId': '25',
#   'liveBroadcastContent': 'none',
#   'defaultLanguage': 'ru',
#   'localized': {'title': 'Фишман про ответ ФБК Кацу',
#    'description': '«Если Максим Кац заботился о своей репутации, то она потерпела довольно серьёзный ущерб». \n\nГость: \nМихаил Фишман — https://www.instagram.com/fishmanmish \n\nВедущая: \nНино Росебашвили — @ninorosebashvili  \n\nСмотрите полный выпуск по ссылке: https://youtube.com/live/zHIAXdIqxKc \n\n💳 Стать патроном любимой передачи: https://www.patreon.com/Popularpolitics \n💰 Спонсировать канал на YouTube: https://www.youtube.com/c/Popularpolitics/join \n💸 Поддержать нас криптовалютой: https://donate.fbk.info/#crypto \n💶 Все способы поддержки в одном месте: https://donate.fbk.info \n\n📖 Заказать книгу Алексея Навального «Патриот»: https://patriot.navalny.com \n\nВажные ссылки: \n🔹 Оформите пожертвование в поддержку политзаключенных: https://june12.io \n🔹 Бот «Напиши политзеку»: https://t.me/politzekam_bot \n🔹 Штабы Навального. Защищенная платформа для активистов в России: https://shtab.navalny.com \n🔹 Наш проект «Цены сегодня». Отслеживаем рост цен в магазинах с начала войны: https://pricing.day \n🔹 Бот-предложка команды Навального: https://t.me/teamnavalny_bot \n\nПоддержите нашу работу! \n🔸 Нажмите кнопку «Спасибо» под этим видео, чтобы поддержать команду за кадром! \n🔸 Поддерживайте Штабы Навального: https://www.patreon.com/shtab_navalny \n🔸 Покупайте мерч Команды Навального: https://navalny.shop \n\nПодписывайтесь, чтобы узнавать о главном раньше других: \n➖ Телеграм: https://t.me/politica_media \n➖ Инстаграм: https://instagram.com/politica_media \n➖ Твиттер (X): https://twitter.com/politica_media \n➖ Помощь юристов и ответы на главные вопросы о мобилизации в телеграм-канале: https://t.me/mobilizationnews \n➖ Новости без цензуры: телеграм-канал «Сирена»: https://t.me/news_sirena \n➖ YouTube-канал «Самое важное» с Иваном Ждановым, где вас ждёт лучшая аналитика событий недели: https://www.youtube.com/@samoe_vazhnoe \n\n#популярнаяполитика #кац #фишман'},
#   'defaultAudioLanguage': 'ru'},
#  'statistics': {'viewCount': '45880',
#   'likeCount': '1177',
#   'favoriteCount': '0',
#   'commentCount': '2118'}}