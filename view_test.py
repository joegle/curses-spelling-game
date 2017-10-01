#!/usr/bin/env python2

import engine as game
import logging
import curses

class Test():
    def __init__(self, screen):
        self.view = game.GameView(screen)
        self.model = game.GameModel()

    def hello_test(self):
        logging.info("foo test")
        self.view.run()


logging.basicConfig(format='%(levelname)s: %(message)s',
                    filename='session.log',
                    level=logging.DEBUG)


def main(stdscr):
    test = Test(stdscr)
    test.hello_test()


if __name__ == "__main__":
     curses.wrapper(main)

