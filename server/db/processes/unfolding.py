from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Annotated, Optional

from .clusterization import Clusterization
from .feature_extraction import FeatureExtraction
from .comment_fetching import CommentSubscription
from .nldr import NLDR

from ..youtube.video import Video
from ..youtube.comment import Comment

# Unfolding
# Revelation
# Disclosure
# Manifestation
# Epiphany
# Unveiling
# Uncovering
# Exhibition

class Unfolding(Document):
  '''Проявление'''
  creation_date: Annotated[datetime, Indexed(default_factory=datetime.now)]
  finish_date: Optional[datetime] = None
  comment_subscription: CommentSubscription
  feature_extraction: FeatureExtraction
  clusterization: Clusterization
  nldr: NLDR
  error: Optional[str] = None
