from client_network import Network


no_data_message = 'Waiting...'
player_color = ''

def main():
    n = Network()
    connect_message = n.connect()
    if connect_message == "Error":
        print('Connection Terminated. Closing program.')
    else:
        print(connect_message)
        if connect_message[-1] == '0':
            player_color = 'white'
        else:
            player_color = 'black'

        while True:
            print(player_color.upper())
            try:
                reply = n.send_receive("SEND FROM " + str(player_color))
                print(reply)
            except:
                break


if __name__ == '__main__':
    main()