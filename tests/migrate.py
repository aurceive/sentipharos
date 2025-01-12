from pymongo import MongoClient
from datetime import datetime

# Подключение к базе данных MongoDB
client = MongoClient("mongodb+srv://admin:admin@sentipharos.nnvrgyb.mongodb.net/?retryWrites=true&w=majority&appName=Sentipharos")
db = client["sentipharos"]  # Замените на ваше имя базы данных
collection = db["Comment"]  # Замените на имя коллекции

# Чтение всех документов из коллекции где info is None
documents = list(collection.find({"info": None}))

# Функция для преобразования документа
def transform_document(doc):
  # Создаем новую структуру с CommentInfo
  comment_info = {
    "info_date": datetime.now(),
    "text_display": doc.get("text_display"),
    "text_original": doc.get("text_original"),
    "author_display_name": doc.get("author_display_name"),
    "author_profile_image_url": doc.get("author_profile_image_url"),
    "author_channel_url": doc.get("author_channel_url"),
    "author_channel_id": doc.get("author_channel_id"),
    "like_count": doc.get("like_count", 0),
    "published_at": doc.get("published_at"),
    "updated_at": doc.get("updated_at"),
  }
  
  # Новый формат документа
  new_doc = {
    "comment_id": doc.get("comment_id"),
    "info": comment_info,
    "video": doc.get("video"),
    "embedding": doc.get("embedding"),
  }
  return new_doc

# Обновление документов в коллекции
for doc in documents:
  # Преобразование документа
  new_doc = transform_document(doc)
  
  # Обновление документа в базе данных
  collection.replace_one({"_id": doc["_id"]}, new_doc)

print("Миграция завершена!")
