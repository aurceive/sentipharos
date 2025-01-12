import asyncio
from datetime import datetime
from typing import Optional
from beanie import Document, Indexed

class Task(Document):
  creation_date: datetime = Indexed(default_factory=datetime.now)
  do_after: Optional[datetime] = Indexed(default=None)
  start_date: Optional[datetime] = Indexed(default=None, partialFilterExpression={"start_date": None})
  end_date: Optional[datetime] = None
  error: Optional[str] = None

  # @property
  # def status(self) -> Literal["pending", "in_progress", "done", "error"]:
  #   if self.error: return "error"
  #   if self.end_date: return "done"
  #   if self.start_date: return "in_progress"
  #   return "pending"

  async def body(self):
    raise NotImplementedError

  @classmethod
  async def fetch_next_task(cls) -> Optional["Task"]:
    '''Асинхронный метод получения следующей задачи'''
    motor_cls = cls.get_motor_collection()
    return await motor_cls.find_one_and_update(
      {"start_date": None, "do_after": {"$lte": datetime.now()}},
      {"$set": {"start_date": datetime.now()}},
      sort=[("creation_date", 1)],
    )
  
  @classmethod
  async def handler(cls, toggle: list[bool]):
    '''Асинхронный обработчик задач'''
    while toggle[0]:
      task = await cls.fetch_next_task()
      if task:
        try:
          await task.body()
        except Exception as e:
          task.error = str(e)
        task.end_date = datetime.now()
        await task.save()
      else:
        await asyncio.sleep(10)