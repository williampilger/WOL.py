<!DOCTYPE html>
<?php
    /*
    * by: will.i.am  |  github.com/williampilger
    *
    * 2023.06.13 - Bom Princípio - RS
    * ♪ Slow It Down | Alok
    *  
    * List devices to start.
    * 
    */
    require_once __DIR__.'/_local/config.php';
    header('Content-Type: text/html; charset=utf-8');
    require_once LOCAL_DIR.'/WOL_device.php';
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
        foreach(WOL_device::list() as $device)
        {
            ?>
            <a class="device-item" href="create.php?device=<?=$device->id?>">
                <h2><?=$device->device_name?></h2>
                <span><?=$device->device_mac?></span>
            </a>
            <?php
        }
        ?>
    </main>
</body>
</html>