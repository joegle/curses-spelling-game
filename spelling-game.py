#!/usr/bin/env python2

import argparse

class game():
    def __init__(self, args):
        print "init"
        self.wordlist = self.load()
        
    def start(self):
        print "started"
        for word in self.wordlist:
            prompt = "\n$ %s\n> " % (word)
            answer = raw_input(prompt)

            if answer == word:
                print "CORRECT!"

    def load(self):
        f = open('word-list.txt','r')
        r1 = map(str.rstrip, f.readlines())
        return map(lambda x:x.lower(), r1)


        
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
parser.add_argument('-c','--config', help="config folder")

parser.add_argument('command', type=str, nargs='?', help="'add' or 'rm'")

args = parser.parse_args()


def main():
    session = game(args)
    session.start()

if __name__ == "__main__":
    main()
    
