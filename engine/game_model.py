#!/usr/bin/env python2

class GameModel():
    """handles game session data and is an extention of the filesystem"""
    
    def __init__(self):
        self.model = []
        self.wordlist = []
        self.schedules = {}

    def __str__(self):
        return "game model"

    
