import socket
from _thread import *
import sys

# data that can be sent to clients
WAITING_FOR_OPPONENT = 'Waiting for opponent'
WAITING_FOR_TURN = 'Waiting for turn'
ERROR = 'Error'
OPPONENT_DISCONNECTED = 'Opponent disconnected'

# data that can be received from clients
CLIENT_WAIT = 'Waiting for game to start'
CLIENT_READY = 'Ready'

server = "192.168.1.3"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def threaded_client(conn, player):
    # initial message on connection, sends the player #
    conn.send(str.encode("Connected as player " + str(player)))

    while True:
        # # check opponent is still connected
        # if player == 0:
        #     if player_connected[1] is False:
        #         conn.sendall(str.encode(OPPONENT_DISCONNECTED))
        # else:
        #     if player_connected[0] is False:
        #         conn.sendall(str.encode(OPPONENT_DISCONNECTED))


        try:
            data = conn.recv(2048).decode()

            if not data:
                # for some reason, no data was received
                print("Disconnected")
                break

            else:
                # client is waiting for confirmation that the game has begun
                if data == CLIENT_WAIT:
                    if player == 0:
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
                    if player == 0 and player_data[1] is not None:
                        # reply with opponent's move data, clear data
                        reply = player_data[1]
                        player_data[1] = None
                    elif player == 1 and player_data[0] is not None:
                        reply = player_data[0]
                        player_data[0] = None

                    # opponent did not make a move yet
                    else:
                        reply = WAITING_FOR_TURN

                # client has sent move data
                else:
                    # save move data
                    player_data[player] = data
                    reply = WAITING_FOR_TURN

                print("Received from player " + str(player) + ": ", data)
                print("Sending to player " + str(player) + ": ", reply)

            conn.sendall(str.encode(reply))

        except:
            break

    print("Lost connection")
    conn.close()


    global playerNum
    playerNum -= 1
    player_connected[playerNum] = False


# index 0: white player, index 1: black player
playerNum = 0
player_data = [None, None]          # stores move data received from the turn player
player_connected = [False, False]   # boolean for whether players have connected

while True:
    conn, addr = s.accept()

    if playerNum <= 1:
        print("Connected to:", addr, "as player ", playerNum)
        start_new_thread(threaded_client, (conn, playerNum))
        player_connected[playerNum] = True
        playerNum += 1
    else:
        # more than 2 players, disconnect immediately
        conn.send(str.encode(ERROR))
        conn.close()
