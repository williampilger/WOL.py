<!DOCTYPE html>
<?php
    require_once __DIR__.'/_local/config.php';
    header('Content-Type: text/html; charset=utf-8');
    require_once LOCAL_DIR.'/WOL_device.php';
?>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WakeUp on LAN</title>
    <style>

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
            <?
        }
        ?>
    </main>
</body>
</html>