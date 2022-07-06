import sys
import socket
import time
from sessions import *

if len(sys.argv) != 3:
    print("Correct usage : python3 server.py <host> <port>")
    sys.exit()

HOST, PORT = sys.argv[1], int(sys.argv[2])

listen_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
listen_socket.bind((HOST, PORT))
listen_socket.settimeout(2)


"""
Sessions
"""

sessions_list = list()
session_threads = list()
current_session_index = 0 # The index of the current session
sessions_list.append(Session(current_session_index))
while True:

    try:
        data, addr = listen_socket.recvfrom(2048)

        data = data.decode()

        if data == "new":

            print("Adding {}:{} to session {}\n".format(addr[0], addr[1], current_session_index))
            sessions_list[current_session_index].add_member(Member(addr))
            if len(sessions_list[current_session_index]) >= 2: # Creates new session when current one is full
                print("Creating a new session and starting current one")
                sessions_list[current_session_index].start()
                current_session_index += 1
                sessions_list.append(Session(current_session_index))

        else:
            msg = data.split(":")
            if len(msg) == 4:
                try:
                    sessions_list[int(msg[0])].update_player(msg)
                except Exception as e:
                    print(str(e) + "player {}".format(msg[1]))
                    time.sleep(1)


    except socket.timeout:
        print("No incoming connection \r", end="")