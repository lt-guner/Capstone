from client_network import Network

# data that can be received from server
WAITING_FOR_OPPONENT = 'Waiting for an opponent'
WAITING_FOR_TURN = 'Waiting for turn'
ERROR = 'Error'
OPPONENT_DISCONNECTED = 'Opponent disconnected'

# data that can be sent to server
WAITING_GAME_START = 'Waiting for game to start'
READY = 'Ready'

# buffer to store move data
make_move = None        # this client has made a move to send to opponent
opponent_move = None    # received move made by opponent

def main():
    n = Network()

    # establish connection and receive first
    connect_message = n.connect()
    if connect_message == ERROR:
        print('Connection Terminated. Game is already full.')
    else:
        print(connect_message)
        if connect_message[-1] == '0':
            player_color = 'white'
            is_turn = True
        else:
            player_color = 'black'
            is_turn = False

        # initial message: waiting for server to indicate game is ready
        message = WAITING_GAME_START
        while True:
            try:
                n.send(message)
                reply = n.receive()

                print('Sending to server:', message)
                print('Received from server:', reply)

                # # opponent disconnected. disconnect and reconnect to start a new game
                # if reply == OPPONENT_DISCONNECTED:
                #     reconnect_message = n.reconnect()
                #     if reconnect_message == ERROR:
                #         print('Connection Terminated. Game is already full.')
                #     else:
                #         print(reconnect_message)
                #         if reconnect_message[-1] == '0':
                #             player_color = 'white'
                #             is_turn = True
                #         else:
                #             player_color = 'black'
                #             is_turn = False

                # server is waiting for an opponent to connect
                if reply == WAITING_FOR_OPPONENT:
                    # continue to wait
                    message = WAITING_GAME_START

                # server is waiting for a move
                elif reply == WAITING_FOR_TURN:
                    # this client's turn
                    if is_turn:
                        global make_move
                        # no move data to send
                        if make_move is None:
                            message = READY

                        # has move data to send
                        else:
                            print("SENDING MOVE TO SERVER")
                            # ready move data, empty move data buffer, end turn
                            message = make_move
                            make_move = None
                            is_turn = False     # can be changed with how game engine tracks turn

                    # not this client's turn
                    else:
                        global opponent_move
                        # no move data received from opponent
                        if opponent_move is None:
                            # stay ready
                            message = READY

                        # received move data from opponent
                        else:
                            # store opponent move data into buffer
                            opponent_move = reply
                            opponent_move = None

                            # update game state in game engine and UI
                            print("RECEIVED OPPONENT MOVE FROM SERVER")

                            # start turn, send ready message
                            is_turn = True      # can be changed with how game engine tracks turn
                            message = READY

            except:
                break


if __name__ == '__main__':
    main()