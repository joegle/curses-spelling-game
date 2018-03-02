#!/usr/bin/env python2
# Copyright 2017 Joseph Wright <joe@joegle.com>

import os
import logging
import time
import datetime
import util
import numpy as np
import pandas as pd
import random

class GameModel():
    """handles game session data and is an extention of the filesystem"""
    
    def __init__(self, config_folder = ".spelling/"):
        self.model = []
        self.config_folder = config_folder
        self.wordlist_file = "/word-list.txt"
        self.score_file = "/score.txt"

        self.average_speed = None
        self.average_accuracy = None
        self.wordlist = []
        self.schedules = {}
        self.setup_config_folder()
        self.load_scores2()
        self.load_words()
        self.compute_stats()

        

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
        r3 = filter(None, r2)
        logging.info("wordlist: " + str(r3))
        self.wordlist = r3

    def load_scores2(self):

        score_file_name = self.config_folder + self.score_file
        
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
            pd = {}
            
            pd["date"] = date
            pd["attempts"] = attempts
            pd["duration"] = duration
            pd["speed"] = speed
            pd["accuracy"] = accuracy
            
            #print word, point

            d = datetime.datetime.fromtimestamp(date).date()

            if d in self.usage:
                self.usage[d].append(date)
            else:
                self.usage[d] = [date]
                
            
            if word in self.schedules:
                self.schedules[word].append(pd)
            else:
                self.schedules[word] = [pd]

        f.close()

    def profile(self, word):
        if word in self.schedules:
            points = self.schedules[word]
        else:
            return
        df = pd.DataFrame(points)
        print df
        average_speed =  df["speed"].mean()
        average_accuracy =  df["accuracy"].mean() 

        print "speed std", df["speed"].std()
        print "accuracy std", df["accuracy"].std()

        print average_speed 
        print average_accuracy 

    def generate_schedule(self):
        words = []
        for x in range(3):
            random.shuffle(self.wordlist)
            words.extend(self.wordlist)
        return words
        
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

    def compute_stats(self):
        self.load_scores2()
        words = self.schedules.keys()
        
        counter = 0
        sum_speed = 0
        sum_accuracy = 0
        for x in words:

            for point in self.schedules[x]:
                sum_speed += point["speed"]
                sum_accuracy += point["accuracy"]
                counter += 1

        self.average_accuracy = sum_accuracy/ counter
        self.average_speed = sum_speed / counter
        
    
    def stats(self):
        self.compute_stats()

        print "date, seconds, count"
        for x in sorted(self.usage.keys()):
            dots = sorted(self.usage[x])
            sum2 = util.spans2(dots)
            print "%s, %s, %s"%(x, sum2, len(self.schedules.keys()))
            
            
        print "# avg speed", self.average_speed
        print "# avg accuracy", self.average_accuracy
            

