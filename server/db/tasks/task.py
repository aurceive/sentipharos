from typing import List, Literal, Optional
from beanie import Document

class Task(Document):
  status: Literal["pending", "in_progress", "done", "error"] = "pending"
  error: Optional[str] = None
  
  async def do(self):
    raise NotImplementedError
  
  @classmethod
  async def next(cls) -> Optional["Task"]:
    return await cls.find_one(cls.status == "pending", nesting_depth=1)

