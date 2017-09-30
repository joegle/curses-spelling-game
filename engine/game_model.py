#!/usr/bin/env python2
import os
import logging

class GameModel():
    """handles game session data and is an extention of the filesystem"""
    
    def __init__(self, config_folder = ".spelling/"):
        self.model = []
        self.config_folder = config_folder
        self.wordlist_file = "/word-list.txt"
        self.score_file = "/score.txt"

        self.wordlist = []
        self.schedules = {}
        self.setup_config_folder()

    def __str__(self):
        return "game model"

    def setup_config_folder(self):
        """create the config folder and data files if needed"""

        config_dir = self.config_folder
        
        logging.info("using config folder: %s" % (config_dir))
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)

        try:
            f = open(config_dir + self.wordlist_file,'r')
        except IOError:
            f = open(config_dir + self.wordlist_file,'a+')
        f.close()

        try:
            f = open(config_dir + self.score_file,'r')
        except IOError:
            f = open(config_dir + self.score_file,'a+')
        f.close()

    def load_words(self):
        logging.info("loading words")

        file_name = self.config_folder + self.wordlist_file

        f = open(file_name, 'r')

        r1 = map(str.rstrip, f.readlines())
        r2 = map(lambda x:x.lower(), r1)
        logging.info("wordlist: " + str(r2))
        self.wordlist = r2
