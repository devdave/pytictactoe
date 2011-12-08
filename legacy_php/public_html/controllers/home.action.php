<?php
/**
 *Server side tic-tac-toe handler
 *with ghetto fabulous AI
 *
 */

class homeAction{
    const maxY = 2;
    const maxX = 2;
    
    const unsetBlock = 'UNSET';
    const playerCode = 'P';
    const cpuCode = 'C';
    
    private $grid = null;
    
    /**
     *
     *Checks to see if this class has a spot in session for its stuff
     *then checks to see if the game grid is in session, if not create it.
     */
    function __construct(){
                
        //setup our cubby hole for class related session data
        if(!isset($_SESSION[__CLASS__]))
            $_SESSION[__CLASS__] = array();
            
        if(isset($_SESSION[__CLASS__]['grid']) && is_array($_SESSION[__CLASS__]['grid'])) {
            $this->grid = &$_SESSION[__CLASS__]['grid'];
        }else{
            $this->reset();
        }
    }
    
    /**
     *Resets or sets in some cases the tic tac toe board
     *
     */
    function __reset(){
        //Could concievably embed the first call into the second for one line maddness.
        $line = array_fill(0,3,homeAction::unsetBlock);                
        $_SESSION[__CLASS__]['grid'] = array_fill(0,3,$line);
        $this->grid = & $_SESSION[__CLASS__]['grid'] ;
        unset($line);                 
        #var_dump($grid,$this->grid); die;
        
    }
    /**
     *Last ditch effort to make sure grid state was saved
     */
    function __destruct(){
        $_SESSION[__CLASS__]['grid'] = $this->grid;        
    }
    
    /**
     *Start of actual Controller actions     
     */
        
    /**
     *Load up the initial view, all actions after this will be through ajax
     */
    function index(){                
        include(VIEWS . "/home/initial.view.php");        
    }
    
    function reset(){
        $this->__reset();
        $this->index();
    }
    
    /**
     *Brutally simple, run through the grid 9^9 times looking for an empty spot.
     *also array_rand isn't safe to use right now *http://bugs.php.net/bug.php?id=45301
     *
     */
    function __cpuMove(){
           for($i = 0 ; $i < 81; $i++){
                
                $x = rand(0,homeAction::maxX);
                $y = rand(0,homeAction::maxY);
                if($this->grid[$x][$y] == homeAction::unsetBlock) {
                    $this->grid[$x][$y] = homeAction::cpuCode;
                    return compact('x','y');
                }
           }
           
        return false;
    }
    
    /***
     *Somewhat generic method to search for winning combinations ( horz/vert/diag across)
     *@param who is either homeAction::playerCode||cpuCode
     *
     */
    function checkWinner($who = homeAction::playerCode){
        
        //Horz check
        for($x = 0; $x < homeAction::maxX ; $x++){
            $lineCount = array_count_values($this->grid[$x]);
            if(isset($lineCount[$who]) and $lineCount[$who] == 3){
            
                return true;
            }            
        }
        //Vert check
        for($y = 0; $y < homeAction::maxY ; $y++){
            $lineCount = array_count_values(array($this->grid[0][$y],$this->grid[1][$y], $this->grid[2][$y] ));
            
            if(isset($lineCount[$who]) && $lineCount[$who] >= 3){
             
                return true;
            }
        }
        //Diagonal Check
        
        //if they don't have the center then they don't have a diagonal
        if($this->grid[1][1] != $who) {
            return false;        
        }else{
            //sigh - no more nify hacks left in the bag
            //Note middle has already been tested
            //is it right to left diagonal?
            if($this->grid[0][0] == $who && $this->grid[2][2] == $who) {                
                return true;
            
            }
            if($this->grid[2][0] == $who && $this->grid[0][2] == $who) {                
                return true;            
            }
            
        }
        return false;
        
        
        
    }
    
    
    /**
     *Handle the player putting a piece somewhere
     *Note, we subtract 1 off the coordinates to escape the event of 0 being eaten in the routing process
     *@todo fix/replace router?
     *@param x = X coordinate
     *@param y = y coordinate
     */
    function move($x = null, $y = null){
        //normalize inputs
        $x--;
        $y--;
        //Setup the scoreboard/state
        $goodMove = false;
        $cpuMove  = false;
        $oldState = null;
        $cpuWins = false;
        $playerWins = false;
        
        //Progressively check to make sure the variables needed are in fact set and the target value is assigned as UNSET
        if(isset($this->grid[$x],$this->grid[$x][$y]) && $this->grid[$x][$y] === 'UNSET'){
            //Just in case, keep a copy
            $oldState = $this->grid[$x][$y];
            $this->grid[$x][$y] = homeAction::playerCode;
            $goodMove = true;
            //Did we win?
            $playerWins = $this->checkWinner();
            if($playerWins == false){
                //Now do the cpu's turn
                //It's brute force AI :)
                $cpuMove = $this->__cpuMove();
                $cpuWins = $this->checkWinner(homeAction::cpuCode);
            }
            
        }else{
            //Something has gone drastically wrong here!!! or someone clicked a position thats already owned
            //@todo add in logic to check for player||cpu ownership of target and then chatise the user
            $goodMove = false;   
        }
                        
        //debug_this $grid = $this->grid;
        header('content-type: application/json');
        //@todo Consolidate cpu | player wins?
        echo json_encode(compact('goodMove','cpuMove','x','y','cpuWins','playerWins'));
    }
    /**
     *Ultra-secret squirrel debug method
     *Used to
     */
    function dumpState(){
        var_dump($this);
        echo "<pre>";
        echo "Player wins: " . $this->checkWinner(), "\n";
        echo "CPU wins: " . $this->checkWinner('C');
    }
}