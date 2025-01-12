from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Annotated, Optional

from .feature_extraction import FeatureExtraction

from ..youtube.video import Video
from ..youtube.comment import Comment

class CommentCluster(BaseModel):
  centroid: list[float]
  comments: list[Comment]

class Clusterization(Document):
  '''Кластеризация'''
  creation_date: Annotated[datetime, Indexed(default_factory=datetime.now)]
  execution_date: Optional[datetime] = Indexed(default=None, partialFilterExpression={'execution_date': None})
  feature_extraction: FeatureExtraction
  video: Video
  algorithm: str
  clusters: list[CommentCluster]
  error: Optional[str] = None