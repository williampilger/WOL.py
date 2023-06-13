<?php
/*
* by: will.i.am  |  github.com/williampilger
*
* 2023.06.13 - Bom Princípio - RS
* ♪ Slow It Down | Alok
*  
* Endpoint responsible to list open WOL Jobs.
* 
*/
require_once __DIR__.'/_local/config.php';
require_once LOCAL_DIR.'/WOL_job.php';
require_once LOCAL_DIR.'/tools.php';

if(log_operacoes) $microtimeStart = microtime(true);
$status = 500;
try
{
    $jobs = WOL_job::list('queue');
    $result = [
        'jobs' => arrayToArray($jobs)
    ];
    $status = 200;
}
catch(Exception $e)
{
    $status = 506; // Internal Error/Conflict
    internalLOG(6, 'Exception in \''.__FILE__.'\' e=\''.$e->__toString().'\'.');
}
if(log_operacoes)
{
    $microtimeTotal = microtime(true) - $microtimeStart;
    internalLOG(11, "[$microtimeTotal s] ".__FILE__."( ".json_encode($_POST)." ) -> status='".$status."'");
}

if(isset($result)){
    echo json_encode($result);
}

http_response_code($status);

?>