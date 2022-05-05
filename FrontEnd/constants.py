WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS
PIECE_IMG_SIZE = 60

RED = (255,0,0)
#WHITE = (255,255,255)
#BLACK = (0,0,0)
BLUE = (0,0,255)
DARK_BROWN = (209, 139, 71)
LIGHT_BROWN = (255, 206, 158)
GREEN = (0,255,0)


# constants for chess game (add chess engine constants here)
WHITE = 'w'
BLACK = 'b'

# constants for sockets
# socket connection parameters
SERVER = '128.193.36.41'     # change to ip address of where server is run
PORT = 5555

# server-to-client messages
WAITING_FOR_OPPONENT = 'Waiting for an opponent'
WAITING_FOR_TURN = 'Waiting for turn'
ERROR = 'Error'
OPPONENT_DISCONNECTED = 'Opponent disconnected'

# server terminal messages
SERVER_START = 'Server Started... Waiting for a connections'

# client-to-server messages
WAITING_GAME_START = 'Waiting for game to start'
READY = 'Ready'

# client terminal messages
GAME_FULL = 'Connection Terminated. Game is already full.'
CONN_SUCCESS = 'Connected to server'
LOST_CONN_RECONN = 'Connection lost... reconnecting'
RECONN_SUCCESS = 'Reconnection successful'