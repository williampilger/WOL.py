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

    /**
     * Instanciate an existent user. ID=0 means a new user.
     * @param int $id user ID.
     * @param mysqli_row $row MySQLi query row (Informed only when user ID = 0, for instantiate the user with query row)
     */
    public function __construct(string $id = '', $row = null)
    {
        if($id != '')//existent register
        {
            if( ! $this->load_instance($id, $includeDeleted))
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
        internalLOG(10, 'Code 22007_2206241427.');
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
        internalLOG(10,'22007_2211011648 - Not implemented.');
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
    public static function list( array $filters = [], bool $includeInactive = false) : array
    {
        $arr = [];

        internalLOG(10,'6512649984651 - Not implemented');
        
        return $arr;
    }

    // #####################################################################################################################
    // # Métodos PRIVADOS - Métodos PRIVADOS - Métodos PRIVADOS - Métodos PRIVADOS - Métodos PRIVADOS - Métodos PRIVADOS - #
    // #####################################################################################################################

    /**
     * Get the informed instance ID from disk
     * @param string JOB ID
     */
    private function load_instance($id, $includeDeleted = false)
    {
        internalLOG(2, '22007_2206161517 - Not implemented');
        return false;
    }

    // #####################################################################################################################
    // # Métodos PRIVADOS ESTÁTICOS - Métodos PRIVADOS ESTÁTICOS - Métodos PRIVADOS ESTÁTICOS - Métodos PRIVADOS ESTÁTICOS #
    // #####################################################################################################################

    /**
     * Pesquisa padrão
     * @param string $filter Pesquisa que deve ser aplicada.
     * @param boolean $includingExcluded Em True quando devem ser considerados registros excluidos de usuários. 
     */
    private static function req_standardQuery($filter, $includingExcluded = False)
    {
        internelLOG(10,'16451326451320 - Not impleented');
        return false;
    }

}

?>