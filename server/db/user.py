from beanie import Document, Indexed
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated, Optional

class User(Document):
  '''Пользователь'''
  creation_date: Annotated[datetime, Indexed(default_factory=datetime.now)]
  email: str = Indexed(unique=True)
  password: str
  first_name: str
  last_name: str
  role: str