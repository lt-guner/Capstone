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
    # initial message on connection, sends the player #
    conn.send(pickle.dumps("Connected as player " + str(playerNum)))

    while True:
        # opponent is disconnected, tell connected player
        # if is_opponent_disconnected(playerNum):
        #     conn.sendall(pickle.dumps(OPPONENT_DISCONNECTED))
        if False:
            pass
        # evaluate message from client and send appropriate response
        else:
            try:
                data = pickle.loads(conn.recv(2048))

                # for some reason, no data was received
                if not data:
                    print("Disconnected from player", playerNum)
                    break

                else:
                    # if isinstance(data, str):
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
                        print('RECEIVED MOVE FROM PLAYER', playerNum)
                        # save move data
                        player_data[playerNum] = data
                        reply = WAITING_FOR_TURN

                    # print("Received from player " + str(playerNum) + ": ", data)
                    # print("Sending to player " + str(playerNum) + ": ", reply)

                conn.sendall(pickle.dumps(reply))

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
        # check if a player is reconnecting (has the same ip address)
        if player_connected[0] is False and addr == player_ip[0]:
            print("Reconnected to:", addr, "as player 0")
            start_new_thread(threaded_client, (conn, 0))
        elif player_connected[1] is False and addr == player_ip[1]:
            print("Reconnected to:", addr, "as player 1")
            start_new_thread(threaded_client, (conn, 1))

        # initial connection
        else:
            print("Connected to:", addr, "as player", playerCount)
            player_connected[playerCount] = True
            player_ip[playerCount] = addr
            start_new_thread(threaded_client, (conn, playerCount))

        playerCount += 1

    elif playerCount == 0:
        # reset player variables; essentially prepare for a new game
        player_data = [None, None]
        player_connected = [False, False]
        player_ip = [None, None]

    # more than 2 players, disconnect new connections immediately
    else:
        conn.send(pickle.dumps(ERROR))
        conn.close()
