from client_network import Network

# data that can be received from server
WAITING_FOR_OPPONENT = 'Waiting for opponent'
WAITING_FOR_TURN = 'Waiting for turn'
ERROR = 'Error'
OPPONENT_DISCONNECTED = 'Opponent disconnected'

# data that can be sent to server
WAITING_GAME_START = 'Waiting for game to start'
READY = 'Ready'

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
                print(reply)

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

                # server is waiting to connect to an opponent
                elif reply == WAITING_FOR_OPPONENT:
                    # continue to wait
                    message = WAITING_GAME_START

                # server is waiting for a move
                elif reply == WAITING_FOR_TURN:
                    # this client's turn, set move data
                    if is_turn:
                        if player_color == 'white':
                            print("MAKING MOVE FOR", player_color.upper())
                            message = 'e2 to e4'
                        else:
                            print("MAKING MOVE FOR", player_color.upper())
                            message = 'd7 to d5'

                        # end turn
                        is_turn = False

                    # not this client's turn
                    else:
                        # stay ready
                        message = READY

                # gameplay, received a move message
                else:
                    print('RECEIVED MOVE FROM OPPONENT. STARTING TURN...')
                    # start turn
                    # use move data to update game state
                    is_turn = True
                    message = READY

            except:
                break


if __name__ == '__main__':
    main()