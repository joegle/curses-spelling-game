#!/usr/bin/env python2
import curses
from curses import panel
import logging

class GameView():
    """Handles the curses display"""

    def __init__(self, screen):
        self.view = []
        self.screen = screen
        self.win_panel = []
        self.setup_screen(screen)
        
    def setup_screen(self, screen):
        logging.debug("Setting up screen")
        self.screen = screen

        curses.curs_set(0)
        screen_y, screen_x = self.screen.getmaxyx()
        win = curses.newwin(screen_y, screen_x, 0, 0)
        self.main_window = panel.new_panel(win)

    def echo_bar(self, text):
        self.main_window.window().move(0,0)
        self.main_window.window().clrtoeol()
        self.main_window.window().addstr(0,0, "echo: " + text, curses.A_BOLD)

    def run(self):
        self.echo_bar("test")
        self.main_window.show()
        c = self.main_window.window().getch()
        
    def __str__(self):
        return "game view"
    
def main(stdscr):
    print stdscr
    view = GameView(stdscr)
    view.run()

if __name__ == "__main__":
    curses.wrapper(main)

