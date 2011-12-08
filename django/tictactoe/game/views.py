from django.http import HttpResponse
from json import dumps

import sys
from os.path import dirname, abspath, join
#Quick hack to re-use the same Game logic class across all frameworks
sys.path.append( abspath(join(dirname(__file__), "../../..") ))
from t3game import T3Game


def init(request):
    """
        Initializes the game logic on the server side
    """
    
    board = T3Game.reset([])
    request.session['board'] = board
    
    response = dict(success = True, board = board )
    return HttpResponse( dumps(response), content_type = "application/json" )
    

def move(request, x, y):
    """
        returns a JSON object that
            must contain bool success, [...] board
                in error must contain str error
                on win must contain str msg, bool game_end
    """
    
    x = int(x)
    y = int(y)
    response = dict(success = False, board = None)
    
    board = request.session.get('board', T3Game.reset(None))
    board, player_won, error = T3Game.player_move(board, x, y)
    
    if error:
        response['error'] = error    
    
    elif player_won == True:
        response['success'] = True
        response['board'] = request.session['board']
        response['msg'] = "Success! You beat the super smart Tic-Tac-Toe AI but the Princess is in another castle."
        response['game_end'] = True
        
    else:
        board, cpu_won, error = T3Game.cpu_move(board)
        
        if error:
            response['error'] = error
            
        elif cpu_won == True:
            response['success'] = True
            response['board'] = request.session['board']
            #Trademarks are there for comedic effect and are not applicable
            response['msg'] = "Somehow the Brute Force (tm) AI of Doom! (tm) has conquered you at Tic-Tac-Toe"
            response['game_end'] = True
    
    
    request.session['board'] = board
    response['board'] = board
    response['success'] = 'error' not in response
    return HttpResponse(dumps(response), content_type = "application/json")
    
    
