import os
import sys
import logging

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.view import view_config

from paste.httpserver import serve

logging.basicConfig()
log = logging.getLogger(__file__)

here = os.path.dirname(os.path.abspath(__file__))

#Hackery for TicTacToe
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), "./../../")) )
try:
    from t3game import T3Game
except ImportError:
    print "Given %s to sys.path[] = %s, still wasn't able to import T3Game" % ( abspath(join(dirname(__file__), "./../../")), sys.path, )
    sys.exit(1)

#Setup logic for serving index.html
_static_index = open(os.path.join(here, "./../../view/index.html")).read()
_static_index_response = Response(content_type = "text/html", body = _static_index)


@view_config(route_name="index")
def index_view(context, request):
    return _static_index_response

@view_config(route_name="init", renderer="json", xhr=True)
def init_view(context, request):
    session = request.session
    board = T3Game.reset([])
    session['board'] = board        
    
    #json_out tools will take this and convert it to valid JSON and set appropriate headers
    return dict(success = True, board = board )

@view_config(route_name="move", renderer="json", xhr = True)
def move_view(context, request):
    session = request.session
    x = int(request.matchdict['x'])
    y = int(request.matchdict['y'])
    
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
    response['x'] = x
    response['y'] = y
    response['success'] = 'error' not in response
    return response
    
    


if __name__ == '__main__':
    # configuration settings
    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True
    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_route('index', "/")
    config.add_route('move', "/move/{x}/{y}")
    config.add_route('init', "/init")
    config.scan()
    # serve app
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0')
