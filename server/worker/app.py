from .video import main as video
from .comment import main as comment
import asyncio

async def main():
  await asyncio.gather(video([True]), comment([True]))

if __name__ == "__main__":
  asyncio.run(main())

# python -m server.worker.app