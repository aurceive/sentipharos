from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from pymongo import IndexModel

from ..youtube.video import Video

class CommentSubscription(Document):
  '''Подписка на извлечение комментариев'''
  creation_date: datetime = Indexed(default_factory=datetime.now)
  end_date: Optional[datetime] = None
  first_comment_fetched: bool = False
  video: Video
  # user: User
  error: Optional[str] = None
  
  class Settings:
    indexes = [
      IndexModel('video', unique=True, partialFilterExpression={'end_date': None})
    ]
    # Уникально по video и user
    # indexes = [
    #   IndexModel(['video', 'user'], unique=True)
    # ]