from random import shuffle

class T3Game(object):
    """
        Written as a stateless collection of static methods for simplicity
    """
    
    MAX_X = 2 #Zero based indexs
    MAX_Y = 2

    POS_OPEN = 0
    POS_AI = 1
    POS_USER = 2    
    
    POS_MAP = { 0:"Open", 1 : "AI", 2 : "User" }
    
    @classmethod
    def reset(cls, board = None):
        """
            Create blank 3x3 grid
            Opted for a manual construct versus list comprehension cleverness
            : board is superflous 
        """
        board = [[cls.POS_OPEN,cls.POS_OPEN,cls.POS_OPEN],[cls.POS_OPEN,cls.POS_OPEN,cls.POS_OPEN],[cls.POS_OPEN,cls.POS_OPEN,cls.POS_OPEN]]
        return board
    
    @classmethod
    def I2C(cls, i):
        """
            Convert an integer to a coordinate in a 3x3 quadrant
        """
        MAX_S = 3
        x = i / MAX_S
        y = i - (x*MAX_S)
        return x,y

    @classmethod
    def player_move(cls, board, x, y):
        return cls.move(board, cls.POS_USER, x, y )
    
    @classmethod
    def cpu_move(cls, board):
        """
            Marvel in the glory of my truly amazing AI skillz
            
            Same return as cls.move
        """
        tests = range(0,9)
        shuffle(tests)
        
        for i in tests:
            x,y = cls.I2C(i)
            if board[x][y] == cls.POS_OPEN:
                break
        else:
            #If we hit this, there are 0 open positions, game is gridlocked
            return board, False, "Stale mate!"
        
        return cls.move(board, cls.POS_AI, x,y)
        
        
        
    @classmethod
    def move(cls, board, who, px, py):
        """
            :board
            :px Player X
            :py Player y
            Returns ([[],...] board, bool player_wins, mixed error)
                if player_wins == True that was a winning move
                if error != Null it will be simple str error message
        """
        
        oldState = board[:]
        try:
            if board[px][py] == cls.POS_OPEN:
                board[px][py] = who
            else:
                return oldState, False, "%s:%s already set to " % (px, py, )
                
        
        except IndexError:
            return oldState, False, "%s:%s out of bounds" % (px, py, )
    
        return board, cls.WinCheck(board, who) , None
    
    @classmethod
    def WinCheck(cls, board, pos_type):
        """
            Returns True if there is a winning state present
        """
        winState = [pos_type, pos_type, pos_type]
        #Horz check
        for x in range(0,3):
            if board[x] == winState:
                return True
        
        #vert check
        for y in range(0,3):
            if [board[0][y], board[1][y], board[2][y] ] == winState:
                return True
        
        #diagonal
        if board[1][1] != pos_type:
            #They don't have the center, so no chance for diagonal
            return False
        else:
            if board[0][0] == pos_type and board[2][2] == pos_type:
                #upper left to lower right
                return True
            elif board[2][0] == pos_type and board[0][2] == pos_type:
                #lower left to upper right
                return True
        
        return False

if __name__ == '__main__':
    from unittest import TestCase, main
    
    class TestT3Game(TestCase):
        board = None
        
        
        def test_simple_win(self):
            board = T3Game.reset()
            board, won, error = T3Game.player_move(board,0,0)
            assert won == False
            board, won, error = T3Game.player_move(board,1,0)
            assert won == False
            board, won, error = T3Game.player_move(board,2,0)
            assert won == True
        
        def test_cpu_shouldwin(self):
            """
                Resolved a bad under range check in WinCheck
            """
            board = T3Game.reset()
            board, won, error = T3Game.move(board, T3Game.POS_AI, 2,0)
            assert won == False
            board, won, error = T3Game.move(board, T3Game.POS_AI, 2,1)
            assert won == False
            board, won, error = T3Game.move(board, T3Game.POS_AI, 2,2)
            assert won == True
    main() 
    
    