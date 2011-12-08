#Stdlib imports
from os.path import (abspath, dirname, join, exists,)
import sys

#Cherrypy imports
import cherrypy
from cherrypy.lib.static import serve_file

#Path hackery to bring the TicTacToe game logic from out of path
sys.path.append(abspath(join(dirname(__file__), "..")))
try:
    from t3game import T3Game
except ImportError:
    print "Given %s to sys.path[] = %s, still wasn't able to import T3Game" % ( abspath(join(dirname(__file__), "..")), sys.path, )
    sys.exit(1)
        
        


class Root(object):
    INDEX_FILE = abspath(join(dirname(__file__), "../view/index.html"))
            
    @cherrypy.expose             
    def index(self):                    
        return serve_file(self.INDEX_FILE, content_type = "text/html")
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def move(self, x, y):
        x = int(x)
        y = int(y)
        response = dict(success = False, board = None)
        
        board = cherrypy.session.get("board", T3Game.reset(None) )
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
        
        
        cherrypy.session['board'] = board
        
        response['board'] = board
        response['success'] = 'error' not in response
        return response
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def init(self):
        board = T3Game.reset([])
        cherrypy.session['board'] = board        
        
        #json_out tools will take this and convert it to valid JSON and set appropriate headers
        return dict(success = True, board = board )
    


conf = {"/" : \
            {
                "tools.sessions.on": True,
                "tools.sessions.storage_type": "file",
                "tools.sessions.storage_path": abspath(join(dirname(__file__), "sessions")),
                "tools.sessions.timeout": 60            
            }
        }

if __name__ == '__main__':
    
    
    assert exists( Root.INDEX_FILE ), "Static index file index.html is missing given path %s" % Root.INDEX_FILE
    
    cherrypy.quickstart(Root(), "/", config = conf)