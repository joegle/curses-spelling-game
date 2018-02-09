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
        self.logo_panel()
        c = self.main_window.window().getch()
        log.info(c)
        
    def __str__(self):
        return "game view"

    def logo_panel(self):
        """create panel for the home screen and bring to front"""
        screen_y, screen_x = self.screen.getmaxyx()
        win = curses.newwin(screen_y, screen_x, 0, 0)

        self.start_panel = panel.new_panel(win)
        f = open("logo.txt", 'r').read()
        self.start_panel.window().addstr(f, curses.A_BOLD)
        logo_height = len(f.split("\n"))
        start_msg = "Press any key to start"
        self.start_panel.window().addstr(logo_height, 2, start_msg, curses.A_BOLD)
        self.start_panel.top()
        self.main_window.bottom()

        self.pflush()

    def pflush(self):
        """refresh the panels"""

        panel.update_panels()
        curses.doupdate()

def main(stdscr):
    print stdscr
    view = GameView(stdscr)
    view.run()

if __name__ == "__main__":
    curses.wrapper(main)

