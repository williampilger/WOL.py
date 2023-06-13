<!DOCTYPE html>
<?php
    /*
    * by: will.i.am  |  github.com/williampilger
    *
    * 2023.06.13 - Bom Princípio - RS
    * ♪ The Red | Chevelle
    *  
    * Consult JOB status.
    * 
    */
    require_once __DIR__.'/_local/config.php';
    header('Content-Type: text/html; charset=utf-8');
    require_once LOCAL_DIR.'/WOL_job.php';
?>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WakeUp on LAN</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        body main{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        body main .device-item{
            padding: 10px;
            border: 1px solid gray;
            border-radius: 7px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
    </style>
</head>
<body>
    <h1>WakeUp on LAN</h1>
    <main>
        <?php
        $id = $_GET['id'] ?? false;
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
                ?>
                <div class="device-item">
                    <h2><?=$job->device_name?></h2>
                    <span>Status: <?=$job->status?></span>
                </div>
                <?php
                if($job->status == 'queue')//if in queue, reload page until 2s, to show new status
                {
                    ?>
                    <script>
                        function refreshPage() {
                            setTimeout(function() {
                                location.reload();
                            }, 2000);
                        }

                        window.onload = function() {
                            refreshPage();
                        };
                    </script>
                    <?php
                }
            }
            else
            {
                ?>
                <span>WOL JOB NOT FOUND</span>
                <?php
            }
        }
        else
        {
            ?>
            <span>MINIUM FIELDS NOT PROVIDED</span>
            <?php
        }
        ?>
    </main>
</body>
</html>