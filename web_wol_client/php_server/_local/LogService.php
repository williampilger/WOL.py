<?php

require_once __DIR__.'/config.php';
require_once __DIR__.'/tools.php';



class LogService
{
    const LOGS_DIR = __DIR__.'/LOG';

    const TYPES = [
        'GERAL',                // 0 - General LOGs.
        'CRITICAL_SECURITY',    // 1 - For errors resulting from probable attacks or attempt to access restricted functions/services. (In cases where in normal use it could hardly happen.)
        'ERRO',                 // 2 - Errors in general (usually caused from user provide wrong data)
        'FATAL_ERROR',          // 3 - Flaws that likely caused incorrect storage of information in the database or wrong system configuration. Should not happen under normal conditions and should be remedied soon.
        'SQL_QUERY',            // 4 - Normals SQL Query run.
        'SQL_QUERY_FAIL',       // 5 - Failed SQL query attempt (such as value overflows, unfilled fields, etc.). They must not occur under normal system operation. They must be investigated immediately.
        'EXCEPTION',            // 6 - Unhandled error log. It needs to be investigated immediately.
        'LOGIN',                // 7 - Default login record. Only logged in login SUCCESS. If you're looking for login failures, look at PHP_WS login logs.
        'DICT_ERROR',           // 8 - Errors occurred while getting translations from WS. It should not happen under normal conditions of use. Investigate soon.
        'LARGEDELETE',          // 9 - Standard large-volume data delete log (with throttling turned off). Under normal conditions, it is unlikely to occur (It is foreseen in cases of failure to create organizations, for example.).
        'DEV',                  // 10- An attempt was made to access an undeveloped or unfinished function.
        'PHP_WS',               // 11- Default PHP service usage log. It happens whenever a request is made to WS.
        'ADM',                  // 12- Use of exclusive functions for system administrators (Internal Authenty use only).
        'DEVAUX',               // 13- Auxiliary Log. Not used in production, just for testing. (Example: complete SQL Query, for when it breaks).
        'GATEWAY_NOTIFICATION', // 14- Notifications from payment gateways
        'ALERT'                 // 15- Occurs when functions are called under unusual circunstancies (you can suspect if this is repeated)
    ];

    /**
     * Função padrão para gravação de novo registro.
     * @param type {int} Identificador do TIPO DA OPERAÇÃO.
     * @param data {string} Conteúdo do LOG a ser registrado.
     */
    public static function reg($type, $data, $userID = 0, $appID = 0)
    {   
        if(is_numeric($type))
        {
            $type = LogService::TYPES[$type];
        }

        $dir = LOGS_DIR;
        $fileName = $dir.'/'.@date('Y').@date('m').@date('d').'.txt';

        $ip = $_SERVER['REMOTE_ADDR'];
        if(is_array($data)) $data = json_encode($data);
        $data = preg_replace('/\s+/', ' ', trim($data));
        $browser = getUserBrowser();
        $os = getUserOS();

        $linha = @date('[d/m/Y H:i:s]');
        $linha .= "\t".$appID;
        $linha .= "\t".$type;
        $linha .= "\t$ip\t$userID\t$data";
        $linha .= "\t$browser\t$os";
        $linha .= "\t".LOG_SESSID."\r\n";

        if(! is_dir($dir))
        {
            mkdir($dir, 0777);
        }

        $file = null;
        if(file_exists($fileName))
        {
            $file = fopen($fileName, 'a');
        }
        else
        {
            $file = fopen($fileName, 'w');
        }
        fwrite($file, $linha);
        fclose($file);
    }

    public static function getLogs($file, int $inireg=0) {
        $fileName = isset($file) ? LOGS_DIR.'/'.anti_injection($file) : null;

        if(is_file($fileName))
        {
            $file = file($fileName);
            $cont = 0;
            $result = [];
            foreach($file as $linha) {
                $cont ++;
                if($cont < $inireg) continue;
                $log = [];
                $linha = explode("\t", str_replace(array("\r", "\n"), "", $linha));
                $dataHora = str_replace(array("[", "]"), array("", ""), explode(" ", $linha[0]));
                $log['date'] = $dataHora[0];
                $log['time'] = $dataHora[1];
                $log['application'] = intval($linha[1]);
                $log['op'] = $linha[2];
                $log['ip'] = $linha[3];
                $log['user'] = intval($linha[4]);
                $log['infos'] = $linha[5];
                $log['browser'] = $linha[6];
                $log['os'] = $linha[7];
                $log['reqid'] = $linha[8];
                if (!empty($linha[9])) $log['solvedTime'] = $linha[9];
                if (!empty($linha[10])) $log['solvedBy'] = $linha[10];
                if (!empty($linha[11])) $log['solved'] = $linha[11] == 'true';
                if (!empty($linha[12])) $log['comment'] = $linha[12];
                $log['id'] = $cont;
                $result['logs'][] = $log;
            }
            $result['count'] = $cont - 1;
            return $result;
        }
    }
    /**
    *Envio do status de um log para um arquivo
    *@param id {int} id do log.
    *@param solved {boolean} status da resolução do log.
    *@param comment {string} Comentário feito pelo usuário sobre o log.
    *@param user {string} usuário que enviou o comentário.
    */
    public static function send_comment($id, $solved, $comment, $user, $file): bool {
        if (is_file($file)) {
            
            $counter = 1;
            $pass = false;

            
            $lines = file($file);
            foreach ($lines as &$line) {
                if ($counter == $id) {
                    $now = (new \DateTime())->format('Y-m-d H:i:s');
                    if ($counter == $id) {
                        $newline = str_replace(array("\r", "\n"), "", $line);
                        $p = 0;
                        for($i=0;$i<=8;$i++){
                            $p = strpos($newline, "\t", $p+1);
                            if( $p === false ) {
                                break;
                            }
                            if($i==8) 
                            {
                                $newline = substr($newline, 0, $p);
                                break;
                            }

                        }
                        $commentline = "\t{$now}\t{$user}\t{$solved}\t{$comment}\r\n";
                        $line = str_replace($line, $newline.$commentline, $line);
                    }
                    $pass = true;
                }
                file_put_contents($file, implode('', $lines));
                $counter ++;
            }

            // while( !feof($logfile) )
            // {
            //     $line = fgets($logfile);
            //     if ($counter == $id) {
            //         $now = (new \DateTime())->format('Y-m-d H:i:s');
            //         $solved = $solved ? 'TRUE' : 'FALSE';
            //         $line = "\t{$now}\t$id\t{$user}\t{$solved}\t{$comment}\r\n";
            //         fwrite($logfile, $line);
            //         fclose($logfile);
            //         $pass = true;
            //         break;
            //     }
            //     $counter ++;
            // }
            return $pass;
        }
        else
        {
            internalLOG(2,'22007_2303081556 - Impossible open LOG file.');
        }
        return false;
    }   
}
?>
