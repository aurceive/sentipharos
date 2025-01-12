from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Annotated, Optional

from .comment_fetching import CommentSubscription
from ..youtube.video import Video
from ..youtube.comment import Comment

class FeatureExtraction(Document):
  '''Извлечение признаков'''
  creation_date: Annotated[datetime, Indexed(default_factory=datetime.now)]
  finish_date: Optional[datetime] = None
  model: str
  comment_subscription: CommentSubscription
  comments: list[Comment]
  error: Optional[str] = None
