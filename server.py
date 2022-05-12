import socket
from _thread import *
import sys
import pickle
from FrontEnd.constants import *
from Chess.move import Move

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER, PORT))
except socket.error as e:
    str(e)

s.listen(2)
print(SERVER_START)

def is_opponent_disconnected(playerNum):
    """
    Returns a boolean for whether the playerNum's opponent is connected or not.
    """
    # for player 0, if player 1 is not connected and has an ip address
    if playerNum == 0 and player_connected[1] is False and player_ip[1]:
        return True
    elif playerNum == 1 and player_connected[0] is False and player_ip[0]:
        return True
    return False

def threaded_client(conn, playerNum):
    """
    Creates a thread to send/receive data to each player.
    """
    global playerCount, player_data, player_connected

    # initial message on connection, sends the player #
    conn.send(pickle.dumps("Connected as player " + str(playerNum)))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            # for some reason, no data was received
            if not data:
                print("Disconnected from player", playerNum)
                break

            # check if opponent has disconnected
            elif game_start and (not player_connected[0] or not player_connected[1]):
                reply = OPPONENT_DISCONNECTED
                print("Player " + str(playerNum) + "'s opponent has disconnected")

            # elif is_opponent_disconnected(playerNum):
            #     reply = OPPONENT_DISCONNECTED
            #     print("Player " + str(playerNum) + "'s opponent has disconnected")

            else:
                # client is waiting for confirmation that the game has begun
                if data == WAITING_GAME_START:
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
                elif data == READY:
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

                # client has sent Move object
                else:
                    print('Received move from player', playerNum)
                    # save move data
                    player_data[playerNum] = data
                    reply = WAITING_FOR_TURN

            # print("Received from player " + str(playerNum) + ": ", data)
            # print("Sending to player " + str(playerNum) + ": ", reply)

            conn.sendall(pickle.dumps(reply))

        except:
            print("Lost connection with player", playerNum)
            break

    conn.close()

    # player disconnected, updates playerNum and player_connected variables
    playerCount -= 1
    player_connected[playerNum] = False


# index 0: white player, index 1: black player
playerCount = 0
player_data = [None, None]          # stores move data received from the turn player
player_connected = [False, False]   # boolean for whether players have connected
player_ip = [None, None]            # stores the ip address of connected clients
game_start = False

while True:
    conn, addr = s.accept()

    # both players disconnected or quit, reset data buffers for a new game
    if player_connected[0] is None and player_connected[1] is None:
        player_data = [None, None]
        player_connected = [False, False]
        player_ip[playerCount] = [None, None]

    if playerCount <= 1 and player_ip[1] is None:
            print("Connected to:", addr, "as player", playerCount)
            player_connected[playerCount] = True
            player_ip[playerCount] = addr
            start_new_thread(threaded_client, (conn, playerCount))
            playerCount += 1

            if playerCount == 1:
                game_start = True

    # more than 2 players, disconnect new connections immediately
    else:
        conn.send(pickle.dumps(ERROR))
        conn.close()

