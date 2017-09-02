#!/usr/bin/env python2

import argparse
import sys
import signal
import os
import timeit
import time

class game():
    def __init__(self, parsed_args):
        print "init"
        self.args = parsed_args
        self.wordlist_file = "word-list.txt"
        self.schedules = {}
        self.wordlist = self.load()

        signal.signal(signal.SIGINT, self.on_quit)

    def start(self):
        print "started"

        print self.args.command
        if self.args.command:
            command = self.args.command

            if command[0] == "add":
                print "adding word"

                self.add_word(command[1])
                sys.exit(0)

            if command[0] == "rm":
                print "removing word"
                sys.exit(0)

        else:
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
                print "CORRECT! %s %s" % (attempts, elapsed)
                return {"word": word, "attempts": attempts, "time": elapsed}

    def record_score(self, score):
        file_name = self.args.config + '/score.txt'
        score_file = open(file_name,'a+')
        epoch_time = int(time.time())
        entry = "%s %s %s %s\n" % ( epoch_time, score['word'], score['attempts'], score['time'])
        score_file.write(entry)
        score_file.close()

    def add_word(self, word):
        file_name = self.args.config + '/word-list.txt'
        word_list = open(file_name,'a+')
        word_list.write(word + "\n")
        word_list.close()

    def load(self):
        print "loading config"

        print "using config folder: %s" % (self.args.config)
        if not os.path.isdir(self.args.config):
            os.mkdir(self.args.config)


        self.load_scores()

        file_name = self.args.config + '/word-list.txt'

        try:
            f = open(file_name, 'r')
        except IOError:
            f = open(file_name, 'w')

        r1 = map(str.rstrip, f.readlines())
        return map(lambda x:x.lower(), r1)

    def load_scores(self):
        """Load scores from file and map into dictionary of words with challenge records"""
        file_name = self.args.config + '/score.txt'
        score_file = open(file_name, 'r')

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
        print "Good bye"
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


def main():
    session = game(args)
    session.start()

if __name__ == "__main__":
    main()

