<?php
/*
 * by: will.i.am                   |  github.com/williampilger
 *
 * 2023.06.12 - São Leopoldo - RS
 * ♪ Take on Me | Ariel, Zoey & Eli
 *
 * Configurações do WS PHP.
 * 
 */



/**
 * ########################
 * # Minimum Headers      #
 * ########################
 */
mb_internal_encoding("UTF-8");
date_default_timezone_set("Brazil/East");
header('Content-type: application/json, *; charset=utf-8'); //Será quase sempre esse o header, quando não for basta sobrescrever.


/**
 * ########################
 * # PHP INISETS          #
 * ########################
 */
ini_set("precision", 14);
ini_set("serialize_precision", -1);
error_reporting(0);//Error reporting desativado pra evitar de invasores conseguirem ter 'ajuda' do debugger do PHP.



/**
    * ########################
    * # LOG CONFIG           #
    * ########################
 */
require_once __DIR__.'/LogService.php';
define('LOG_SESSID', generateRandomString(5));//Used to identificate a unique request.
function internalLOG($type, $data)
{
    if(is_array($data)) $data = json_encode($data);
    LogService::reg($type, $data);
}




/**
     * ########################
     * # GENERAL FUNCTIONS    #
     * ########################
 */

// Hora atual, em segundos.
function getNowTimeStamp()
{
    $hora = new DateTime();
    return $hora->getTimestamp();
}
define('INI_TIME_STAMP', getNowTimeStamp());

/**
     * ########################
     * # GENERAL LIBS         #
     * ########################
 */
const LOCAL_DIR = __DIR__;
const DATA_DIR = __DIR__.'/../_data';
const LIB_tools = __DIR__.'/tools.php';

?>