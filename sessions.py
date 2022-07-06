"""
Defines sessions
"""

import socket
import pygame
from pygame.locals import *
import threading
from game_thread import ServerGameThread

class Session:

    def __init__(self, ID):
        
        self.ID =ID
        self.members = list()
        self.started = False
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Define game objects
        self.ball = Rect(392, 392, 16, 16)
        self.player_left = Rect(16, 300, 20, 200)
        self.player_right = Rect(764, 300, 20, 200)
        self.velx = 9
        self.vely = 8

        self.thread = ServerGameThread(self)


    def add_member(self, member):
        self.members.append(member)

    def __len__(self):
        return len(self.members)

    def start(self):
        self.started = True
        playerID = 0
        for member in self.members:
            self.socket.sendto("start:{}:{}".format(self.ID, playerID).encode(), member.address)
            playerID += 1
        self.thread.start()

    def update_player(self, data):

        if data[1] == "0":
            self.player_left.x = int(data[2])
            self.player_left.y = int(data[3])
        elif data[1] == "1":
            self.player_right.x = int(data[2])
            self.player_right.y = int(data[3])

    def game_loop(self):
        while True:
            pass

class Member:

    def __init__(self, address):
        self.address = address