<?php
/*
* by: will.i.am  |  github.com/williampilger
*
* 2023.06.13 - Bom Princípio - RS
* ♪ Slow It Down | Alok
*  
* Endpoint responsible to create a start request (WOL job).
* 
*/
require_once __DIR__.'/_local/config.php';
require_once LOCAL_DIR.'/WOL_device.php';

if(log_operacoes) $microtimeStart = microtime(true);
$status = 500;
try
{
    $id = $_GET['device'] ?? false;
    
    if($id)
    {
        try
        {
            $device = new WOL_device($id);
        }
        catch( Exception $e )
        {
            $device = false;
        }
        if($device)
        {
            $job = $device->createJob();
            if( $job )
            {
                $result = [
                    'msg' => '2306130644 - success on create job',
                    'jobID' => $job
                ];
                internalLOG(2,$result['msg']);
                $status = 200;

                $directory = rtrim(dirname(parse_url( $_SERVER['REQUEST_URI'] , PHP_URL_PATH)), '/\\');
                header("Location: {$directory}/consult.php?id={$job}");
                exit();
            }
            else
            {
                $result = ['msg' => '2306130643 - fail on create job'];
                internalLOG(2,$result['msg']);
                $status = 501;    
            }
        }
        else
        {
            $result = ['msg' => '2306130642 - device not found'];
            internalLOG(2,$result['msg']);
            $status = 404;    
        }
    }
    else
    {
        $result = ['msg' => '2306130641 - Minimum fields not informed'];
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