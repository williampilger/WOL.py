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
require_once LOCAL_DIR.'/WOL_job.php';
require_once LIB_tools;


class WOL_device
{
    const save_dir = DATA_DIR.'/WOL_device';
    const DEFAULT_IP_MASK = '192.168.0.0';
    
    public string $id;
    public string $device_ipmask;
    public string $device_name;
    public string $device_mac;
    public int $created_at;

    /**
     * Instanciate an existent user. ID=0 means a new user.
     * @param int $id user ID.
     * @param mysqli_row $row MySQLi query row (Informed only when user ID = 0, for instantiate the user with query row)
     */
    public function __construct(string $id = '')
    {
        if($id != '')//existent register
        {
            if( ! $this->load_instance($id))
            {
                internalLOG(3, '2306130541 - Unable to instantiate this WOL device');
                throw new Exception("2306130541 - Unable to instantiate this WOL device");
            }
        }
        else
        {
            $this->id = '';//will be filed when it be saved
            $this->device_ipmask = WOL_device::DEFAULT_IP_MASK;
            $this->device_name = 'Standard Device';
            $this->device_mac = '';
            $this->created_at = INI_TIME_STAMP;
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
            } while ( file_exists(WOL_device::save_dir."/{$this->id}"));

        }
        else //UPDATE ENTRY
        {
            unlink( WOL_device::save_dir."/{$this->id}" );
        }

        $file = fopen( WOL_device::save_dir."/{$this->id}", 'w');

        fwrite($file, $this->device_ipmask."\r\n");
        fwrite($file, $this->device_name."\r\n");
        fwrite($file, $this->device_mac."\r\n");
        fwrite($file, $this->created_at."\r\n");
        
        fclose($file);

        return true;
    }

    /**
     * Create a WOL Job to start this device
     * @return false|string
     */
    public function createJob()
    {
        $job = new WOL_job();
        $job->device_ipmask = $this->device_ipmask;
        $job->device_mac = $this->device_mac;
        $job->device_name = $this->device_name;
        if( $job->Save() )
        {
            return $job->id;
        }
        return false;
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
            return unlink( WOL_device::save_dir."/{$this->id}" );
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
            'created_at' => $this->created_at
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
    public static function list( ) : array
    {
        $arr = [];
        
        $entries = scandir( WOL_device::save_dir );
        foreach($entries as $entry){
            if($entry=="."||$entry==".."||$entry=="readme.md") continue;
            $fn = explode('.', $entry);
            if(count($fn) == 1)
            {
                $arr[] = new WOL_device($fn[0]);
            }
            else
            {
                internalLOG(3, '2306130545 - Wrong name format');
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
        if( file_exists(WOL_device::save_dir."/{$id}") )
        {
            $file = WOL_device::save_dir."/{$id}";
            $file = file( $file );
            $this->id = $id;
            $this->device_ipmask = str_replace(["\r","\n"],['',''], $file[0] );
            $this->device_name = str_replace(["\r","\n"],['',''], $file[1] );
            $this->device_mac = str_replace(["\r","\n"],['',''], $file[2] );
            $this->created_at = intval(str_replace(["\r","\n"],['',''], $file[3] ) );
            return true;
        }
        else {
            internalLOG(2, '2306130546 - Not found');
        }

        return false;
    }

    // #####################################################################################################################
    // # Métodos PRIVADOS ESTÁTICOS - Métodos PRIVADOS ESTÁTICOS - Métodos PRIVADOS ESTÁTICOS - Métodos PRIVADOS ESTÁTICOS #
    // #####################################################################################################################

}

?>