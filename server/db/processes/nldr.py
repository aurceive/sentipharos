from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Annotated, Optional

from ..youtube.video import Video
from ..youtube.comment import Comment
from .clusterization import Clusterization

class Position(BaseModel):
  x: float
  y: float

class Point(BaseModel):
  position: Position
  comment: Comment

class PointCluster(BaseModel):
  centroid: Position
  points: list[Point]

class NLDR(Document):
  '''Нелинейное понижение размерности'''
  clusterization: Clusterization
  clusters: list[PointCluster]
  error: Optional[str] = None
