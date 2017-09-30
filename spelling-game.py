#!/usr/bin/env python2
# Copyright 2017 Joseph Wright <joe@joegle.com>

import argparse
import sys
import signal
import os
import timeit
import time
import curses
from curses import panel
import logging
import engine

class game():
    def __init__(self, parsed_args, screen):
        screen.clear()
        logging.info("===== init ====")


        self.model = engine.GameModel(".spelling")
        self.view = engine.GameView()
        logging.info(self.view)
        
        self.screen = screen
        self.win_panel = []
        self.start_panel = []
        self.setup_screen()
        self.logo_panel()
        self.args = parsed_args

        self.load_scores()
        self.load_words()
        self.process_args()
        self.menu()
        signal.signal(signal.SIGINT, self.on_quit)

    def setup_screen(self):
        screen_y, screen_x = self.screen.getmaxyx()
        win = curses.newwin(screen_y, screen_x, 0, 0)
        curses.curs_set(0)
        self.win_panel = panel.new_panel(win)
        self.echo_bar("Init")

    def logo_panel(self):
        """create curses panel for home screen and bring to front"""
        screen_y, screen_x = self.screen.getmaxyx()
        win = curses.newwin(screen_y, screen_x, 0, 0)

        self.start_panel = panel.new_panel(win)
        f = open("logo.txt", 'r').read()
        self.start_panel.window().addstr(f)
        logo_height = len(f.split("\n"))
        start_msg = "Press any key to start"
        self.start_panel.window().addstr(logo_height, 2, start_msg)
        self.start_panel.top()
        self.win_panel.bottom()

        self.pflush()
        
    def pflush(self):
        panel.update_panels()
        curses.doupdate()

    def echo_bar(self, text):
        self.win_panel.window().move(0,0)
        self.win_panel.window().clrtoeol()
        self.win_panel.window().addstr(0, 0, "echo: " + text, curses.A_BOLD)

    def prompt(self, text):
        self.win_panel.window().move(5, 5)
        self.win_panel.window().clrtoeol()
        self.win_panel.window().addstr(5, 5, "prompt: " + text, curses.A_BOLD)

    def menu(self):
        """start screen display and start on key press"""
        c = self.screen.getkey()
        self.start_panel.bottom()
        self.win_panel.top()
        self.pflush()
        self.start()
        
    def process_args(self):
        """switch to do one time commands and possibly exit""" 
        if self.args.command:
            command = self.args.command

            if command[0] == "add":
                logging.info("adding word")

                self.add_word(command[1])
                sys.exit(0)

            if command[0] == "rm":
                logging.info("removing word")
                sys.exit(0)
        
    def start(self):
        self.process_args()
        self.challenge_loop()

    def challenge_loop(self):
        """Main game loop"""
        logging.info("Starting game")
        logging.info(self.model.wordlist)
        for word in self.model.wordlist:
            score = self.challenge_word(word)
            self.record_score(score)
        
    def challenge_word(self, word):
        """runs a typing challenge loop 
            and returns (word, attempts, seconds_elapsed)
        """
        prompt = "\n$ %s\n> " % (word)
        start_time = timeit.default_timer()
        started = True
        attempts = 0
        correct = False
        char_index = 0
        answer = ""

        while started or not correct:
            started = False
            
            self.prompt(word)
            c = self.win_panel.window().getch()
            answer = answer + chr(c)
            
            self.echo_bar(answer)

            attempts += 1
            
            if chr(c) == word[char_index]:

                char_index += 1
                if char_index == len(word):
                    correct = True
                    elapsed = timeit.default_timer() - start_time
                    self.echo_bar("")
                    #self.echo_bar("CORRECT! %s %s" % (attempts, elapsed))
                    return {"word": word, "attempts": attempts, "time": elapsed}
            else:
                correct = False
                char_index = 0
                answer = ""
                curses.beep()
                #self.win_panel.window().refresh()
                self.echo_bar("")

    def record_score(self, score):
        file_name = self.args.config + self.model.score_file
        score_file = open(file_name,'a+')
        epoch_time = int(time.time())
        entry = "%s %s %s %s\n" % ( epoch_time, score['word'], score['attempts'], score['time'])
        score_file.write(entry)
        score_file.close()

    def add_word(self, word):
        file_name = self.args.config + self.model.wordlist_file
        word_list = open(file_name,'a+')
        word_list.write(word + "\n")
        word_list.close()

    def load_words(self):
        logging.info("loading words")

        file_name = self.args.config + self.model.wordlist_file

        f = open(file_name, 'r')

        r1 = map(str.rstrip, f.readlines())
        r2 = map(lambda x:x.lower(), r1)
        logging.info(r2)
        self.model.wordlist = r2

    def load_scores(self):
        """Load scores from file and map into dictionary of words with challenge records"""
        file_name = self.args.config + self.model.score_file
        score_file = open(file_name, 'a+')
        
        for entry in score_file:
            tokens = entry.split()
            word = tokens[1]
            point = (int(tokens[0]), int(tokens[2]), float(tokens[3]))

            if word in self.model.schedules:
                self.model.schedules[word].append(point)
            else:
                self.model.schedules[word] = [point]

        score_file.close()

    def on_quit(self, signal, frame):
        logging.info("Good bye")
        sys.exit(0)

guide = """# Examples
- examples 
- here
"""

parser = argparse.ArgumentParser(description='Spelling game',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=guide)

parser.add_argument('-m','--message', help='Log a message')
parser.add_argument('-t','--test', help="Test run", action='store_true')
parser.add_argument('-a','--add', help="add word to game", action='store_true')
parser.add_argument('-r','--remove', help="remove word from game",
                    action='store_true')
parser.add_argument('-c','--config', help="config folder", default=".spelling/")

parser.add_argument('command', type=str, nargs='*', help="'add' or 'rm'")

args = parser.parse_args()


stdscr = curses.initscr()

logging.basicConfig(format='%(levelname)s: %(message)s',
                    filename='session.log',
                    level=logging.DEBUG)


def main(stdscr):
    session = game(args, stdscr)

if __name__ == "__main__":
    curses.wrapper(main)

