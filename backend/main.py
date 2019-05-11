#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
from typing import Optional, Awaitable
from sys import argv

from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop

# from handlers.history import History
import handlers.history
from lib.db_methods import MongoHandler


class BasicHandler(RequestHandler):
    db_handler = MongoHandler()

    def prepare(self) -> Optional[Awaitable[None]]:
        return super().prepare()

    def on_finish(self) -> None:
        super().on_finish()


def get_app():
    return Application([
        (r'/api/history', handlers.history.History)
    ],
        autoreload=True
        # mongo_handler=MONGO_HANDLER
    )


def run():
    if len(argv) < 2:
        port = 8080
    else:
        try:
            port = int(argv[1])
        except ValueError as ve:
            print("Error: please provide a correct port")
            exit(0)
        else:
            app = get_app()
            try:
                print(f"Started on localhost:{port}")
                app.listen(port)
                IOLoop.current().start()
            except Exception as e:
                print(f"Cannot start server with given port")
                exit(0)


if __name__ == '__main__':
    run()
