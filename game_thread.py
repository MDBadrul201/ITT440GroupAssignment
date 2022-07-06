import threading
import pygame
from pygame.locals import *
import time


class ServerGameThread(threading.Thread):

    def __init__(self, session):
        threading.Thread.__init__(self)
        self.session = session

    def wait(self, t):
        # Send data to left player then to right player, waiting a certain time
        for i in range(t):
            self.session.socket.sendto("{}:{}:{}:{}:{}".format(self.session.ID, self.session.ball.x, self.session.ball.y, self.session.player_right.x, self.session.player_right.y).encode(), self.session.members[0].address)
            self.session.socket.sendto("{}:{}:{}:{}:{}".format(self.session.ID, self.session.ball.x, self.session.ball.y, self.session.player_left.x, self.session.player_left.y).encode(), self.session.members[1].address)
            time.sleep(1)

    def run(self):
        clock = pygame.time.Clock()

        time.sleep(5)
        while self.session.started:
            clock.tick(60)
            self.session.ball.move_ip(self.session.velx, self.session.vely)


            if self.session.ball.x < 0 or self.session.ball.x > 792:
                self.session.velx = 9
                self.session.vely = 8
                self.session.ball = Rect(392, 392, 16, 16)
                self.wait(5)


            if self.session.ball.y < 0:
                self.session.vely = abs(self.session.vely)
            elif self.session.ball.y > 792:
                self.session.vely = -abs(self.session.vely)

            if self.session.ball.colliderect(self.session.player_left):
                self.session.velx = abs(self.session.velx)
                self.session.vely = (self.session.ball.centery - self.session.player_left.centery)*0.05

            elif self.session.ball.colliderect(self.session.player_right):
                self.session.velx = -abs(self.session.velx)
                self.session.vely = (self.session.ball.centery - self.session.player_right.centery)*0.05

            # Send data to left player then to right player
            self.session.socket.sendto("{}:{}:{}:{}:{}".format(self.session.ID, self.session.ball.x, self.session.ball.y, self.session.player_right.x, self.session.player_right.y).encode(), self.session.members[0].address)
            self.session.socket.sendto("{}:{}:{}:{}:{}".format(self.session.ID, self.session.ball.x, self.session.ball.y, self.session.player_left.x, self.session.player_left.y).encode(), self.session.members[1].address)


class ClientGameDataThread(threading.Thread):

    def __init__(self, sessionID, playerID, serverIP, serverPort, ball, player_left, player_right, velx, vely, data_socket):
        threading.Thread.__init__(self)
        self.sessionID = sessionID
        self.playerID = playerID
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.ball = ball
        self.player_left = player_left
        self.player_right = player_right
        self.velx = velx
        self.vely = vely
        self.data_socket = data_socket
        self.started = True

    def quit(self):
        self.started = False

    def run(self):
        while self.started:
            msg = self.data_socket.recv(2048)
            # Check data
            msg = msg.decode()
            data = msg.split(":")
            if len(data) != 5:
                pass
            else:
                self.ball.x = int(data[1])
                self.ball.y = int(data[2])
                if self.playerID == 0:
                    self.player_right.x = int(data[3])
                    self.player_right.y = int(data[4])
                    self.data_socket.sendto("{}:{}:{}:{}".format(self.sessionID, self.playerID, self.player_left.x, self.player_left.y).encode(), (self.serverIP, self.serverPort))
                else:
                    self.player_left.x = int(data[3])
                    self.player_left.y = int(data[4])
                    self.data_socket.sendto("{}:{}:{}:{}".format(self.sessionID, self.playerID, self.player_right.x, self.player_right.y).encode(), (self.serverIP, self.serverPort))



