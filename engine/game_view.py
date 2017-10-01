#!/usr/bin/env python2
import curses
from curses import panel
import logging

class GameView():
    """Handles the curses display"""

    def __init__(self):
        self.view = []
        self.screen = []
        self.win_panel = []

        curses.wrapper(self.setup_screen)
        
    def setup_screen(self, scr):
        logging.debug("Setting up screen")

        self.screen = scr
        
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
    
