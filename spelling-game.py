#!/usr/bin/env python2

import argparse
import sys
import signal
import os
import timeit
import time
import curses
import logging

class game():
    def __init__(self, parsed_args, screen):
        screen.clear()
        logging.info("init")
        self.screen = screen
        self.setup_screen()
        self.args = parsed_args
        self.wordlist_file = "/word-list.txt"
        self.score_file = "/score.txt"
        self.schedules = {}
        self.wordlist = []
        self.setup()
        self.load_scores()
        self.load_words()

        signal.signal(signal.SIGINT, self.on_quit)

    def setup_screen(self):
        screen_y, screen_x = self.screen.getmaxyx()
        win = curses.newwin(screen_y, screen_x, 0, 0)
        self.screen.addstr(0, 0, "Current mode: Typing mode", curses.A_BOLD)
        self.screen.refresh()
        
    def setup(self):
        """create the config folder and data files if needed"""

        logging.info("using config folder: %s" % (self.args.config))
        if not os.path.isdir(self.args.config):
            os.mkdir(self.args.config)

        try:
            f = open(self.args.config + self.wordlist_file,'r')
        except IOError:
            f = open(self.args.config + self.wordlist_file,'a+')
        f.close()

        try:
            f = open(self.args.config + self.score_file,'r')
        except IOError:
            f = open(self.args.config + self.score_file,'a+')
        f.close()

    def start(self):
        logging.info("started")

        logging.info(self.args.command)
        if self.args.command:
            command = self.args.command

            if command[0] == "add":
                logging.info("adding word")

                self.add_word(command[1])
                sys.exit(0)

            if command[0] == "rm":
                logging.info("removing word")
                sys.exit(0)

        else:
            logging.info("Starting game")
            logging.info(self.wordlist)
            for word in self.wordlist:
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

        while started or not correct:
            started = False
            answer = raw_input(prompt)
            attempts += 1

            if answer == word:
                correct = True
                elapsed = timeit.default_timer() - start_time
                logging.info("CORRECT! %s %s" % (attempts, elapsed))
                return {"word": word, "attempts": attempts, "time": elapsed}

    def record_score(self, score):
        file_name = self.args.config + self.score_file
        score_file = open(file_name,'a+')
        epoch_time = int(time.time())
        entry = "%s %s %s %s\n" % ( epoch_time, score['word'], score['attempts'], score['time'])
        score_file.write(entry)
        score_file.close()

    def add_word(self, word):
        file_name = self.args.config + self.wordlist_file
        word_list = open(file_name,'a+')
        word_list.write(word + "\n")
        word_list.close()

    def load_words(self):
        logging.info("loading words")

        file_name = self.args.config + self.wordlist_file

        f = open(file_name, 'r')

        r1 = map(str.rstrip, f.readlines())
        r2 = map(lambda x:x.lower(), r1)
        logging.info(r2)
        self.wordlist = r2

    def load_scores(self):
        """Load scores from file and map into dictionary of words with challenge records"""
        file_name = self.args.config + self.score_file
        score_file = open(file_name, 'a+')
        
        for entry in score_file:
            tokens = entry.split()
            word = tokens[1]
            point = (int(tokens[0]), int(tokens[2]), float(tokens[3]))

            if word in self.schedules:
                self.schedules[word].append(point)
            else:
                self.schedules[word] = [point]

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
    session.start()

if __name__ == "__main__":
    curses.wrapper(main)

