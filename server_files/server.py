import socket
from _thread import *
import sys

# data that can be sent to clients
WAITING_FOR_OPPONENT = 'Waiting for an opponent'
WAITING_FOR_TURN = 'Waiting for turn'
ERROR = 'Error'
OPPONENT_DISCONNECTED = 'Opponent disconnected'

# data that can be received from clients
CLIENT_WAIT = 'Waiting for game to start'
CLIENT_READY = 'Ready'

server = "192.168.1.15"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def threaded_client(conn, playerNum):
    # initial message on connection, sends the player #
    conn.send(str.encode("Connected as player " + str(playerNum)))

    while True:
        # opponent is disconnected
        if playerNum == 0:
            if player_connected[1] is False and player_ip[1]:
                conn.sendall(str.encode(OPPONENT_DISCONNECTED))
        else:
            if player_connected[0] is False and player_ip[0]:
                conn.sendall(str.encode(OPPONENT_DISCONNECTED))

        try:
            data = conn.recv(2048).decode()

            if not data:
                # for some reason, no data was received
                print("Disconnected from player", playerNum)
                break

            else:
                # client is waiting for confirmation that the game has begun
                if data == CLIENT_WAIT:
                    if playerNum == 0:
                        # check if the opponent is connected
                        if player_connected[1] is False:
                            # reply waiting for opponent
                            reply = WAITING_FOR_OPPONENT
                        else:
                            reply = WAITING_FOR_TURN
                    else:
                        if player_connected[0] is False:
                            reply = WAITING_FOR_OPPONENT
                        else:
                            reply = WAITING_FOR_TURN

                # client is waiting to receive move data
                elif data == CLIENT_READY:
                    # check if opponent has move data to send
                    if playerNum == 0 and player_data[1] is not None:
                        # reply with opponent's move data, clear data
                        reply = player_data[1]
                        player_data[1] = None
                    elif playerNum == 1 and player_data[0] is not None:
                        reply = player_data[0]
                        player_data[0] = None

                    # opponent did not make a move yet
                    else:
                        reply = WAITING_FOR_TURN

                # client has sent move data
                else:
                    # save move data
                    player_data[playerNum] = data
                    reply = WAITING_FOR_TURN

                print("Received from player " + str(playerNum) + ": ", data)
                print("Sending to player " + str(playerNum) + ": ", reply)

            conn.sendall(str.encode(reply))

        except:
            break

    print("Lost connection")
    conn.close()

    # player disconnected, updates playerNum and player_connected variables
    global playerCount
    playerCount -= 1
    player_connected[playerNum] = False

# index 0: white player, index 1: black player
playerCount = 0
player_data = [None, None]          # stores move data received from the turn player
player_connected = [False, False]   # boolean for whether players have connected
player_ip = [None, None]

while True:
    conn, addr = s.accept()

    if playerCount <= 1:
        # check if the player is reconnecting (has the same ip address)
        if player_connected[0] is False and addr == player_ip[0]:
            print("Reconnected to:", addr, "as player 0")
            start_new_thread(threaded_client, (conn, 0))
        elif player_connected[1] is False and addr == player_ip[1]:
            print("Reconnected to:", addr, "as player 1")
            start_new_thread(threaded_client, (conn, 1))

        # initial connection
        else:
            print("Connected to:", addr, "as player ", playerCount)
            player_connected[playerCount] = True
            player_ip[playerCount] = addr
            start_new_thread(threaded_client, (conn, playerCount))

        playerCount += 1
    else:
        # more than 2 players, disconnect immediately
        conn.send(str.encode(ERROR))
        conn.close()
