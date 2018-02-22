#!/usr/bin/env python2
# Copyright 2017 Joseph Wright <joe@joegle.com>

import os
import logging
import time
import datetime
import util

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

    def load_scores(self):
        """Load scores from file and map into dictionary of words with challenge records"""
        file_name = self.config_folder + self.score_file

        score_file = open(file_name, 'a+')

        for entry in score_file.readlines():
            tokens = entry.split()
            word = tokens[1]
            point = (int(tokens[0]), int(tokens[2]), float(tokens[3]))

            if word in self.schedules:
                self.schedules[word].append(point)
            else:
                self.schedules[word] = [point]

        score_file.close()

    def load_scores2(self):

        score_file_name = self.config_folder + self.score_file
        
        print "score2", score_file_name

        f = open(score_file_name, "r")

        self.usage = {}
        
        for entry in f.readlines():
            tokens = entry.split()
            date = int(tokens[0])
            word = tokens[1]
            attempts = int(tokens[2])
            b = len(word)
            duration = float(tokens[3])
            speed = attempts * b / duration
            accuracy = attempts**(-1.0/b)
            point = (date, attempts, duration, speed, accuracy)
            #print word, point

            d = datetime.datetime.fromtimestamp(date).date()

            if d in self.usage:
                self.usage[d].append(date)
            else:
                self.usage[d] = [date]
                
            
            if word in self.schedules:
                self.schedules[word].append(point)
            else:
                self.schedules[word] = [point]

        f.close()

        
    def record_score(self, score):
        """write the score to disk"""
        file_name = self.config_folder + self.score_file
        score_file = open(file_name,'a+')
        epoch_time = int(time.time())
        entry = "%s %s %s %s\n" % ( epoch_time, score['word'], score['attempts'], score['time'])
        score_file.write(entry)
        score_file.close()

    def add_word(self, word):
        """add a new word to training set"""

        if word in self.wordlist:
            return "Already in word list"

        file_name = self.config_folder + self.wordlist_file
        word_list = open(file_name,'a+')
        word_list.write(word + "\n")
        word_list.close()
        return None

    def stats(self):
        self.load_scores2()
        k = self.schedules.keys()
        print self.schedules[k[1]]

        counter = 0
        sum_speed = 0
        sum_accuracy = 0
        for x in k:

            for point in self.schedules[x]:
                print point
                sum_speed += point[3]
                sum_accuracy += point[4]
                counter += 1

        print "avg speed", sum_speed/ counter
        print "avg accuracy", sum_accuracy/ counter

        for x in self.usage.keys():
            print "\n>>>>",x
            dots = sorted(self.usage[x])
            r = util.spans(dots)
            sum1 = util.sum_pair(r)
            sum2 = util.spans2(dots)
            print ">",sum1, sum2
            
            if sum1 != sum2:
                print dots
            
        print "stats"
