<?php
/*
 * by: will.i.am                   |  github.com/williampilger
 *
 * 2023.06.12 - São Leopoldo - RS
 * ♪ \Enter One / Sol Seppy
 *  
 * Class responsible to manipulate WOL Jobs.
 * 
 */

require_once __DIR__.'/config.php';
require_once LIB_tools;


class WOL_job
{
    const save_dir = DATA_DIR.'/WOL_job';
    const DEFAULT_IP_MASK = '192.168.0.0';
    
    public string $id;
    public string $device_ipmask;
    public string $device_name;
    public string $device_mac;
    public int $created_at;
    public int $executed_at;
    public string $status; // 'queue' | 'done' | 'fail'

    private string $_db_status;//same that status. But it is the DISK STATUS.

    /**
     * Instanciate an existent user. ID=0 means a new user.
     * @param int $id user ID.
     * @param mysqli_row $row MySQLi query row (Informed only when user ID = 0, for instantiate the user with query row)
     */
    public function __construct(string $id = '' )
    {
        if($id != '')//existent register
        {
            if( ! $this->load_instance($id ))
            {
                internalLOG(3, '2206161430 - Unable to instantiate this WOL Job');
                throw new Exception("2206161430 - Unable to instantiate this WOL Job");
            }
        }
        else
        {
            $this->id = '';//will be filed when it be saved
            $this->device_ipmask = WOL_job::DEFAULT_IP_MASK;
            $this->device_name = 'Standard Device';
            $this->device_mac = '';
            $this->created_at = INI_TIME_STAMP;
            $this->executed_at = 0;
            $this->status = $this->_db_status = 'queue';
        }
    }

    // #####################################################################################################################
    // # Métodos PÚBLICOS - Métodos PÚBLICOS - Métodos PÚBLICOS - Métodos PÚBLICOS - Métodos PÚBLICOS - Métodos PÚBLICOS - #
    // #####################################################################################################################

    /**
     * Save this instance to disk.
     */
    public function Save()
    {
        if($this->id == '') //NEW ENTRY
        {
            do{
                $this->id = generateRandomString(32);
            } while ( file_exists(WOL_job::save_dir."/{$this->id}.queue") || file_exists(WOL_job::save_dir."/{$this->id}.done") || file_exists(WOL_job::save_dir."/{$this->id}.fail"));

        }
        else //UPDATE ENTRY
        {
            unlink( WOL_job::save_dir."/{$this->id}.{$this->_db_status}" );
        }

        $file = fopen( WOL_job::save_dir."/{$this->id}.{$this->status}", 'w');

        fwrite($file, $this->device_ipmask."\r\n");
        fwrite($file, $this->device_name."\r\n");
        fwrite($file, $this->device_mac."\r\n");
        fwrite($file, $this->created_at."\r\n");
        fwrite($file, $this->executed_at."\r\n");
        
        fclose($file);

        $this->_db_status = $this->status;
        return true;
    }

    /**
     * Load JSON information and update this instance
     */
    public function updateFromArray($json, bool $saveChanges = true)
    {
        internalLOG(10, '22007_2207061438 - Not implemented');
        return false;
    }

    /**
     * Delete this instance from disk.
     * HEADS UP! This function directly affects the database.
     */
    public function Delete( )
    {
        if($this->id != '')
        {
            return unlink( WOL_job::save_dir."/{$this->id}.{$this->_db_status}" );
        }
        return false;
    }

    /**
     * Get JSON with complete user account informations.
     * @param bool $includeAvailableItems includes the user subscriptions product=>level.
     * @return bool|array userData;
     */
    public function toArray(bool $includeAvailableItems = true)
    {
        return [
            'id' => $this->id,
            'device_ipmask' => $this->device_ipmask,
            'device_name' => $this->device_name,
            'device_mac' => $this->device_mac,
            'created_at' => $this->created_at,
            'executed_at' => $this->executed_at
        ];
    }

    /**
     * HEADS UP! -> CALL IT ONLY FROM CRON JOBS!
     * 
     * Remove older JOBs
     */
    public static function cron_clearTable( int $maxCount=0 ): bool
    {
        internalLOG(10, "22007_2211011743 - Not implemented");
        return false;
    }

    /**
     * Request users list.
     * This method returns one array with the users instances.
     */
    public static function list( string $status = '' ) : array
    {
        $arr = [];

        $entries = scandir( WOL_job::save_dir);
        foreach($entries as $entry){
            if($entry=="."||$entry==".."||$entry=="readme.md") continue;
            $fn = explode('.', $entry);
            if(count($fn) == 2)
            {
                if($status=='' || $status==$fn[1])
                {
                    $arr[] = new WOL_job($fn[0]);
                }
            }
            else
            {
                internalLOG(3, '2306130517 - Wrong name format');
            }
        }        
        return $arr;
    }

    // #####################################################################################################################
    // # Métodos PRIVADOS - Métodos PRIVADOS - Métodos PRIVADOS - Métodos PRIVADOS - Métodos PRIVADOS - Métodos PRIVADOS - #
    // #####################################################################################################################

    /**
     * Get the informed instance ID from disk
     * @param string JOB ID
     */
    private function load_instance( $id )
    {
        $file = false;
        if( file_exists(WOL_job::save_dir."/{$id}.queue") )
        {
            $file = 'queue';
        }
        else if( file_exists(WOL_job::save_dir."/{$id}.done") )
        {
            $file = 'done';
        }
        else if( file_exists(WOL_job::save_dir."/{$id}.fail") )
        {
            $file = 'fail';
        } else {
            internalLOG(2, '2306130521 - Not found');
        }

        if($file)
        {
            $this->status = $this->_db_status = $file;
            $file = WOL_job::save_dir."/{$id}.{$file}";
            $file = file( $file );
            $this->id = $id;
            $this->device_ipmask = str_replace(["\r","\n"],['',''], $file[0] );
            $this->device_name = str_replace(["\r","\n"],['',''], $file[1] );
            $this->device_mac = str_replace(["\r","\n"],['',''], $file[2] );
            $this->created_at = intval(str_replace(["\r","\n"],['',''], $file[3] ) );
            $this->executed_at = intval(str_replace(["\r","\n"],['',''], $file[4] ) );
            return true;
        }

        return false;
    }

    // #####################################################################################################################
    // # Métodos PRIVADOS ESTÁTICOS - Métodos PRIVADOS ESTÁTICOS - Métodos PRIVADOS ESTÁTICOS - Métodos PRIVADOS ESTÁTICOS #
    // #####################################################################################################################

}

?>