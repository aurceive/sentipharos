# app.py
import os
import tornado.ioloop
import tornado.web
from motor.motor_asyncio import AsyncIOMotorClient


mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://admin:admin@sentipharos.nnvrgyb.mongodb.net/?retryWrites=true&w=majority&appName=Sentipharos")
client = AsyncIOMotorClient(mongo_uri)
db = client.get_default_database()

# class ItemHandler(tornado.web.RequestHandler):
#     async def get(self, item_id=None):

def create_app():
    app = tornado.web.Application([
        (r"/items", ItemHandler),
        (r"/items/([0-9a-fA-F]{24})", ItemHandler),  # маршрут для получения элемента по id
    ])
    port = 8080
    app.listen(port)
    return app


if __name__ == "__main__":
    app = create_app()
    tornado.ioloop.IOLoop.current().start()
