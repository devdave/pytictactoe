<html>
    <head>
        <title>Would you like to play a game?</title>
        <style type="text/css">
            #gameBoard {
                margin-top: 12em;
                margin-left: 35%;                
                float: left;
            }
            
            #gameBoard .gameSpot {
                min-width: 120px;
                height; 15em;
                min-height: 120px;
                float: left;
                border: solid black thin;
            }
            
            #gameBoard .player {
                background-color: red !important;
            }
            
            #gameBoard .cpu {
                background-color: blue !important;
            }
            
            
            #menuBar {
                list-style: none;
                position: absolute;
                top: 0px;
                left: 0px;
                
                background-color: lightblue;                
                min-height: 10px;
                
                padding-left: 10px;
                padding-right: 5px;
                
            }
            
            #menuBar li {                
                margin-right: 5px;
                padding-right: 5px;                
                padding: 5px;
                
                
            }
            .menuItem {
                border-top: solid black thin;
                padding: 2px;                            
            }
            
            .menuItem a:hover {                
                color: red;
            }
            
        </style>
        <script type="text/javascript" src="/js/prototype.js"></script>
        <script type="text/javascript">
                Event.observe(window,'load',function(){
                $$('#menuBar .menuItem').invoke('hide');
                
                $('menuBar').observe('mouseover',function(){
                    $$('#menuBar .menuItem').invoke('show');
                      
                });
                
                $('menuBar').observe('mouseout',function(){
                    $$('#menuBar .menuItem').invoke('hide');                      
                });
                
                $$('.gameSpot').each(function(spot){                  
                    spot.observe('click',function(e){
                        myNode = e.element();
                        var temp = myNode.id.split("_");                        
                        x = Number(temp[1]) + 1;
                        y = Number(temp[2]) + 1;
                        new Ajax.Request("?/home/move/"+x+"/"+y,
                        {
                            method:'get',
                            onSuccess: moveResponse,
                        });
                        
                    })
                });
                
            });
        </script>
        <script type="text/javascript">
        
            function messageBox(message){
                if($('msgBox') == undefined){
                    msgBox = $(document.createElement('span'));
                    msgBox.hide();
                    msgBox.id = "msgBox";
                    $$('body')[0].appendChild(msgBox);
                    msgBox.observe('click',function(ev){
                      ev.element().hide();
                    });
                }
                else
                    msgBox = $('msgBox');
                    
                msgBox.update(message);
                
                msgBox.setStyle({
                    position:'absolute',
                    left: '35%',
                    top: '12%',
                    backgroundColor: 'blue',
                    color:'white',
                    zIndex:'1000'
                })
                
                
                msgBox.show();
                
            }
            
            function flipTile(x,y,who){
                idName = "coord_" + x + "_" + y;
                $(idName).addClassName(who);
            }
            
            function moveResponse(transport){
                
                
                logic = transport.responseJSON;
                if(logic == undefined) {
                    messageBox("There was a syntax/logic error " + transport.responseText );
                }
                
                
                
                if(logic.goodMove){                    
                    flipTile(logic.x,logic.y,'player');
                    if(logic.playerWins == true){
                        alert("Congradulations, you outsmarted the computer");
			location.href="?/home/reset";
                    }
                }else{
                    messageBox("Server said it didn't like that move.");
                    return;
                }
                
                if(logic.cpuMove){
                    if(logic.cpuMove.x != undefined && logic.cpuMove.y != undefined ){
                        flipTile(logic.cpuMove.x, logic.cpuMove.y, 'cpu');
                    }
                    if(logic.cpuWins != undefined && logic.cpuWins == true){
                        alert("Whoa...The server beat you");
			location.href="?/home/reset";
                    return;
                }
                }                
                
            }
            
            
        </script>
    </head>
    <body style="z-index:1">        
        <ul id="menuBar">
            <li>Main menu</li>
            <li class="menuItem"> Source code <a href="/vcon.tar.bz2">here</a></li>
            <li class="menuItem" ><a title="This will reset the board" href="?/home/reset" >Reset</a></li>            
            
        </ul>
        <fieldset id="gameBoard" >
        <!-- This pretty much violates a slew of good practices...but I'm alright with that for here -->
            <? for($x = 0;$x<3;$x++):
                for($y = 0;$y<3;$y++): ?>
                    <div class="gameSpot" id="<?= "coord_{$x}_{$y}" ?>">&nbsp;</div>
                <?endfor; ?>
                <br style="clear:left">
            <?endfor; ?>
        </fieldset>
</body>
</html>
