<?php
/**
 *@package Virtual Console
 *@author Ward, David J <vcon.project@digitalairmen.org>
 *
 *Initialization and front controller
 */
ini_set("display_errors",true);
error_reporting(E_ALL);
$x = session_start();

/**
 *Debugging mechanism
 *Ugly as dirt but extremely lightweight.
 *
 *Switch on by assigning array() else set to false, 1, 'anything' and goes away silently.
 *Justification
 *  dlog could easily be gutted and replaced with a dump to syslog, mysql, a singleton logging class, anything
 *  or inversely be gutted completely and just be dlog(){ return; } which becomes a near zero cost when opcached.
 */
$DEBUG_LOG = array();
function dlog($msg, $type = 'INFO' ){    
    if(is_array($GLOBALS['DEBUG_LOG'])) $GLOBALS['DEBUG_LOG'][] = "$type: $msg";
}




#setup the corner stone of our environment
define('SYSBASE',dirname(__FILE__));
define('VIEWS',       SYSBASE."/views");
define('MISC',	      SYSBASE."/misc");
define('MODELS',      SYSBASE."/models");
define('CONTROLLERS', SYSBASE."/controllers");
define('LIBS',        SYSBASE."/libs");
define('WEBROOT',     SYSBASE."/webroot");


foreach(array('SYSBASE','VIEWS','MISC','MODELS','CONTROLLERS','LIBS') as $testDir ){
    $value = constant($testDir);
    if(!file_exists($value))
        error_log("CONSTANT $testDir did not evaluate correctly");
        
    if(!is_readable($value))
        error_log("$value is not correctly permissioned");
    
    dlog("const($testDir) = '$value'");
}

//Helpers

function isAjax(){
    if(!isset($_SERVER['HTTP_X_REQUESTED_WITH'])) return false;
    
    return $_SERVER['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest';    
}



/**
 *Diet Routing 
 */
$route = strtolower($_SERVER['QUERY_STRING']);
//Default routes
$class = 'home';
$action = 'index';
$arguments = null;

if($route){
    $pieces = explode("/",$route);
    $pieces = array_filter($pieces);
    
    $class = count($pieces) ? array_shift($pieces) : $class;
    $action = count($pieces) ? array_shift($pieces) : $action;
    $arguments = count($pieces) ? $pieces : null;    
}

dlog("\$class=$class \$action = $action");
$className = "{$class}Action";
$classFile = CONTROLLERS."/$class.action.php";

if(file_exists($classFile)){
    include($classFile);
    
    if(class_exists($className)){
        
        $obj = new $className();
        if(method_exists($obj,$action)){
            if(count($arguments))
                call_user_func_array(array($obj,$action),$arguments);
            else
                $obj->$action();
        }else{
            dlog("Unhandled action($action) for controller $class");
            error_log("Unhandled action($action) for controller $class");
        }
    }else{
        error_log("Missing controller class $className");
        dlog("Missing controller class $className");
    }
}else{
    error_log("Could not find correct controller file for $class");
    dlog("Could not find correct controller file for $class");
}


//@todo deprecated as this never happens
if(is_null($route)){
    //run default controller/action
}else{
    
    
}


//Defaults to pumping debug messages to firebug ALWAYS ( client or user )
if(isAjax() == false && is_array($DEBUG_LOG)):?>
<script type="text/javascript">
    if(console != undefined){
    <? foreach($DEBUG_LOG as $line ): ?> console.log("<?=$line?>");            
    <? endforeach; ?>
    }
</script><? endif; 



