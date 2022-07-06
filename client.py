import sys
import socket
import time
import pygame
from game_thread import ClientGameDataThread
from pygame.locals import *

pygame.init()

# Game Data :
sessionID = -1 # Default (should quit if trying to start with negative value)
playerID = -1 # 0 --> left side | 1 --> right side

counter = 0
ball = Rect(392, 392, 16, 16)
player_left = Rect(16, 300, 20, 200)
player_right = Rect(764, 300, 20, 200)
velx = 8
vely = 8


if len(sys.argv) != 3:
    print("Correct usage : python3 server.py <host> <port>")
    sys.exit()


HOST, PORT = sys.argv[1], int(sys.argv[2])


data_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

data_socket.sendto("new".encode(), (HOST, PORT))

wait_for_session_start = True
while wait_for_session_start:
    data, return_address = data_socket.recvfrom(2048)
    print(data.decode())
    # Decode data to start session
    data = data.decode().split(":")
    if data[0] == "start":
        print("Starting session...")
    try:
        sessionID = int(data[1])
        playerID = int(data[2])
        wait_for_session_start = False
    except:
        print("Could not start session.")

    if sessionID < 0:
        wait_for_session_start = False
        print("Session ID is invalid, could not start session.")
    if playerID < 0:
        wait_for_session_start = False
        print("Player ID is invalid, could not start session.")


data_thread = ClientGameDataThread(sessionID, playerID, HOST, PORT, ball, player_left, player_right, velx, velx, data_socket)

data_thread.start()


running = True
# Set up display
screen = pygame.display.set_mode((800, 800))

background = pygame.Surface((800, 800))
background.fill((0, 0, 0))
pygame.draw.rect(background, (255, 255, 255), (0, 0, 800, 800), 8)
pygame.draw.rect(background, (255, 255, 255), (399, 0, 2, 800))

clock = pygame.time.Clock()

while running: # Main game loop
    clock.tick(60)

    for e in pygame.event.get(pump=True):
        if e.type == QUIT:
            running = False
            break
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        running = False
    if keys[K_DOWN]:
        if playerID == 0 and player_left.y < 600:
            player_left.move_ip(0, 7)
        elif player_right.y < 600:
            player_right.move_ip(0, 7)
    if keys[K_UP]:
        if playerID == 0 and player_left.y > 0:
            player_left.move_ip(0, -7)
        elif player_right.y > 0:
            player_right.move_ip(0, -7)
    # Fill background with black
    screen.blit(background, (0,0))

    pygame.draw.rect(screen, (0, 255, 0), ball)
    pygame.draw.rect(screen, (255, 0, 0), player_left)
    pygame.draw.rect(screen, (0, 0, 255), player_right)

    pygame.display.flip()

print("Shutting down")
data_thread.quit()
time.sleep(1)
print(data_thread.started)
data_thread.join()
