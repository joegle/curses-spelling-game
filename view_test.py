#!/usr/bin/env python2

import engine as game
import logging


class Test():
    def __init__(self):
        self.view = game.GameView()
        self.model = game.GameModel()

    def hello_test(self):
        logging.info("foo test")
        self.view.run()


logging.basicConfig(format='%(levelname)s: %(message)s',
                    filename='session.log',
                    level=logging.DEBUG)

if __name__ == "__main__":
    t = Test()
    t.hello_test()

