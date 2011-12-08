#Stdlib imports
from os.path import (abspath, dirname, join, exists,)
import sys

#Bottle imports
import bottle #Kind of odd I admit
from bottle import (route, run, request,)

#3rd party utilities
from beaker.middleware import SessionMiddleware
from contextlib import contextmanager
session_opts = {
    "session.type" : "file",
    "session.cookie_expires" : 300,
    "session.data_dir" : "./data",
    "session.auto" : True    
}

app = SessionMiddleware(bottle.app(), session_opts)

@contextmanager
def GetSession():
    s = request.environ.get("beaker.session")
    yield s
    s.save()
    

#Path hackery to bring the TicTacToe game logic from out of path
sys.path.append(abspath(join(dirname(__file__), "..")))
try:
    from t3game import T3Game
except ImportError:
    print "Given %s to sys.path[] = %s, still wasn't able to import T3Game" % ( abspath(join(dirname(__file__), "..")), sys.path, )
    sys.exit(1)

INDEX_FILE = open(abspath(join(dirname(__file__), "../view/index.html"))).read()

@route("/")
def index():
    return INDEX_FILE

@route("/init")
def init():
    with GetSession() as session:
        board = T3Game.reset([])
        session['board'] = board        
        
        #json_out tools will take this and convert it to valid JSON and set appropriate headers
        return dict(success = True, board = board )

@route("/move/:x/:y")
def move(x,y):
    with GetSession() as session:
        x = int(x)
        y = int(y)
        response = dict(success = False, board = None)
        
        board = session.get("board", T3Game.reset(None) )
        board, player_won, error = T3Game.player_move(board, x, y)
        
        if error:
            response['error'] = error    
        
        elif player_won == True:
            response['success'] = True
            response['board'] = board
            response['msg'] = "Success! You beat the super smart Tic-Tac-Toe AI but the Princess is in another castle."
            response['game_end'] = True
            
        else:
            board, cpu_won, error = T3Game.cpu_move(board)
            
            if error:
                response['error'] = error
                
            elif cpu_won == True:
                response['success'] = True
                response['board'] = board
                #Trademarks are there for comedic effect and are not applicable
                response['msg'] = "Somehow the Brute Force (tm) AI of Doom! (tm) has conquered you at Tic-Tac-Toe"
                response['game_end'] = True
        
        
        session['board'] = board
        
        response['board'] = board
        response['success'] = 'error' not in response
        return response        
    
if __name__ == '__main__':
    bottle.run(app=app)