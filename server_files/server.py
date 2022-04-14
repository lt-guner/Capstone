import socket
from _thread import *
import sys

server = "192.168.1.3"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

no_data_message = 'Waiting...'

# index 0: white player, index 1: black player
playerNum = 0
player_data = [no_data_message, no_data_message]

def threaded_client(conn, player):
    conn.send(str.encode("Connected as player " + str(player)))

    while True:
        try:
            data = conn.recv(2048).decode()
            # store the data from the connection with the appropriate player in their player_data index
            if player == 0:
                player_data[0] = data
            else:
                player_data[1] = data

            if not data:
                print("Disconnected")
                break
            else:
                # send each player data received from the other player's connection
                if player == 0:
                    reply = player_data[1]
                else:
                    reply = player_data[0]

                print("Received from player " + str(player) + ": ", data)
                print("Sending to player " + str(player) + ": ", reply)

            conn.sendall(str.encode(reply))

        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    if playerNum > 1:
        conn.send(str.encode("Error"))
        conn.close()
    print("Connected to:", addr, "as player ", playerNum)
    start_new_thread(threaded_client, (conn, playerNum))
    playerNum += 1
