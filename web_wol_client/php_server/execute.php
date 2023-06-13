<?php
/*
* by: will.i.am  |  github.com/williampilger
*
* 2023.06.13 - Bom Princípio - RS
* ♪ Slow It Down | Alok
*  
* Endpoint responsible to mark a job as done or failed
* 
*/
require_once __DIR__.'/_local/config.php';
require_once LOCAL_DIR.'/WOL_job.php';

if(log_operacoes) $microtimeStart = microtime(true);
$status = 500;
try
{
    $id = $_GET['id'] ?? false;
    $status = $_GET['status'] ?? 'done';

    if($id)
    {
        try
        {
            $job = new WOL_job($id);
        }
        catch(Exception $e)
        {
            $job = false;
        }

        if($job)
        {
            $job->status = $status;
            if( $job->Save() )
            {
                $result = ['msg' => '2306130737 - Successfully update WOL Job'];
                internalLOG(2,$result['msg']);
                $status = 200;
            }
            else
            {
                $result = ['msg' => '2306130738 - Fail on update WOL Job'];
                internalLOG(2,$result['msg']);
                $status = 501;
            }
        }
        else
        {
            $result = ['msg' => '2306130739 - Job not found'];
            internalLOG(2,$result['msg']);
            $status = 401;
        }
    }
    else
    {
        $result = ['msg' => '2306130736 - Minimum fields not informed'];
        internalLOG(2,$result['msg']);
        $status = 401;
    }
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