<?php
/*
 * by: will.i.am                   |  github.com/williampilger
 *
 * 2023.06.12 - São Leopoldo - RS
 * ♪ Make a Memory / Bon Jovi
 *  
 * Biblioteca com funções diversas.
 * 
 */


require_once __DIR__.'/config.php';

/**
 * Gerar string aleatória.
 */
function generateRandomString($length = 10) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}

/**
 * Find out user's browser
 * @param bool $full	if set, return complete information about the browser.
 * 
 * thanks isDesign for this S2.
**/
function getUserBrowser($full = true){
    $userAgent = $_SERVER['HTTP_USER_AGENT'];
    $navegador = 'Desconhecido';
    $versao    = "";

    // Next get the name of the useragent yes seperately and for good reason
    if (preg_match('/MSIE/i', $userAgent) && !preg_match('/Opera/i', $userAgent)) {
        $navegador = 'Internet Explorer';
        $ub        = "MSIE";
    } elseif (preg_match('/Firefox/i', $userAgent)) {
        $navegador = 'Mozilla Firefox';
        $ub        = "Firefox";
    } elseif (preg_match('/Chrome/i', $userAgent)) {
        $navegador = 'Google Chrome';
        $ub        = "Chrome";
    } elseif (preg_match('/Safari/i', $userAgent)) {
        $navegador = 'Apple Safari';
        $ub        = "Safari";
    } elseif (preg_match('/Opera/i', $userAgent)) {
        $navegador = 'Opera';
        $ub        = "Opera";
    } elseif (preg_match('/Netscape/i', $userAgent)) {
        $navegador = 'Netscape';
        $ub        = "Netscape";
    }

    // finally get the correct version number
    $known   = array('Version', $ub, 'other');
    $pattern = '#(?<browser>' . join('|', $known) .
        ')[/ ]+(?<version>[0-9.|a-zA-Z.]*)#';
    if (!preg_match_all($pattern, $userAgent, $matches)) {
        // we have no matching number just continue
    }

    // Version
    if ($full) {
        $i = count($matches['browser']);
        if ($i != 1) {
            //we will have two since we are not using 'other' argument yet
            //see if version is before or after the name
            if (strripos($userAgent, "Version") < strripos($userAgent, $ub)) {
                $versao = $matches['version'][0];
            } else {
                $versao = $matches['version'][1];
            }
        } else {
            $versao = $matches['version'][0];
        }
        // check if we have a number
        if ($versao == null || $versao == "") {
            $versao = " v: ?";
        } else {
            $versao = " v:" . $versao;
        }
    }

    return $navegador . $versao;
}


/**
 * Find out user's OS.
 * 
 * thanks isDesign for this S2.
**/
function getUserOS(){
    $userAgent          = $_SERVER['HTTP_USER_AGENT'];
    $sistemaOperacional = "Desconhecido";

    // Modo Clássico
    // if (preg_match("/linux/i", $userAgent)) {
    //     $sistemaOperacional = "Linux";
    // } elseif (preg_match("/macintosh|mac os x/i", $userAgent)) {
    //     $sistemaOperacional = "MacOS";
    // } elseif (preg_match("/windows|win32/i", $userAgent)) {
    //     $sistemaOperacional = "Windows";
    // }

    //Modo will
    $ini = strpos($userAgent, '(');
    $end = strpos($userAgent, ')');
    if( $ini && $end )
    {
        $sistemaOperacional = substr($userAgent, $ini+1, $end-$ini-1);
    }

    return $sistemaOperacional;
}

/**
 * Print a array in HTML simple text.
 */
function debugPrintArray($array, $ident=0){
	foreach($array as $chave => $elemento){
		$identacao = "";
		for($i=0;$i<$ident; $i++){
			$identacao .= "-----|";
		}
		if($elemento instanceof mysqli_result){			
			echo "$identacao $chave:   MySQLI Result<br>";
		}else if($elemento instanceof mysqli){			
			echo "$identacao $chave:   MySQLI<br>";
		}
		else if(is_array($elemento)){			
			echo "$identacao chave: $chave { <br>";
			debugPrintArray($elemento, ++$ident);
			echo "$identacao }<br>";
			$ident--;
		}else if(is_string($elemento) || is_int($elemento) || is_float($elemento)){
			echo "$identacao $chave:   $elemento<br>";
		}else if(is_bool($elemento)){
			if($elemento){
				echo "$identacao $chave:   true<br>";
			}else{
				echo "$identacao $chave:   false<br>";
			}
		}else if(is_object($elemento)){
			echo "$identacao Métodos do objeto: $elemento { <br>";
			debugPrintArray(get_class_methods($elemento), ++$ident);
			echo "$identacao }<br>";
			$ident--;
		}else if($elemento===null){
			echo "$identacao $chave:   NULL<br>";
			
		}else if(!isset($array)){
			echo "$identacao $chave:  /Vazio/<br>";
		}else{
			echo "$identacao $chave:   Tipo desconhecido<br>";
		}
	}
}

/**
 * This function get a array[Class] to a array os class->toArray()
 */
function arrayToArray( $classArray )
{
    if(is_array($classArray))
    {
        $arr = [];
        foreach($classArray as $class)
        {
            $arr[] = arrayToArray($class); 
        }
        return $arr;
    }
    else
    {
        try
        {
            $out = $classArray->toArray(); 
        }
        catch(Exception $e)
        {
            $out = $classArray;
            internalLOG(6, '22007_2303071432 - Isso não deve acontecer muito. Se se repetir, refazer isso ou descontinuar a função');
        }
        return $out;
    }
}

/**
 * Object Advanced Print.
 * Returns JSON with the object's Variables and Methods names.
 */
function objectAdvPrint($obj)
{
    $arr = [];

    $vars = get_object_vars($obj);
    if($vars) $arr['vars'] = $vars;
    
    $methods = get_class_methods($obj);
    if($methods) $arr['methods'] = $methods;
    
    if(in_array('toArray', $methods)) $arr['toArray'] = $obj->toArray();
    
    return $arr;
}

?>