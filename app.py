# app.py
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world! Your Tornado app is running.")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    port = 8080  # Google Cloud Run использует этот порт по умолчанию
    app.listen(port)
    print(f"Server started on port {port}")
    tornado.ioloop.IOLoop.current().start()
