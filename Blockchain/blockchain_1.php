<?php 
$json = file_get_contents('orders.json');
$status = json_decode($json);
$json_2 = file_get_contents('coffee.json');
$coffee = json_decode($json_2);
$current_status = 1;
foreach ($_POST as $name => $value) {
    $id = $name;
}

$file = 'test.txt';
$current = file_get_contents($file);
$current .= $id;
file_put_contents($file, $current);

?>

<!DOCTYPE html>
<html>
    <head>
        <title>Payment Terminal Interface</title>
        <meta charset="utf-8">
        <link rel="icon" type="image/png" href="https://cdn-icons-png.flaticon.com/512/2091/2091665.png">
        <link rel="stylesheet" href="blockchain.css">
    </head>
    <body>
        <div id="payment_app">
            <div class="main-layout">
                <div class="main-layout__wrap">
                    <img src="https://cdn-icons-png.flaticon.com/512/2091/2091665.png" alt="Blockchain" style="position: relative; top: 1.5em; max-width: 100%; object-fit: contain; height: 72px;">
                    <div class="payment_interface">
                        <div class="main-card">
                            <form action="./blockchain_2.php" method="post">
                                <div class="main-card__header">
                                    <h2 class="main-card__title">Your Order</h2>
                                    <p class="main-card__description">Product: <span style="font-weight: bold;"><?php echo $coffee[$id]->title ?></span></p>
                                </div>
                                <div class="main-card__content">
                                    <input type='hidden' name='id' value='<?php echo $id ?>'>
                                    <div class="input-field" style="margin-bottom: 20px;">
                                        <span style="font-weight: bold;">Quanity</span>
                                        <div class="input-field__wrapper">
                                            <input class="input-field__input" type="number" name="quantity" placeholder="Enter desired quantity" autocomplete="off">
                                        </div>
                                    </div>
                                    <div class="input-field" style="margin-bottom: 20px;">
                                        <span style="font-weight: bold;">Delivery start date</span>
                                        <div class="input-field__wrapper">
                                            <input class="input-field__input" type="date" name="startdate" autocomplete="off">
                                        </div>
                                    </div>
                                    <div class="input-field">
                                        <span style="font-weight: bold;">Delivery end date</span>
                                        <div class="input-field__wrapper">
                                            <input class="input-field__input" type="date" name="enddate" autocomplete="off">
                                        </div>
                                    </div>
                                    <div class="need_help">
                                        Need help?
                                    </div>
                                </div>
                                <div class="main-card__footer">
                                    <div class="main-card__bottom-btn">
                                        <input type="submit" value="Continue" class="main-button main-button--black main-button--full-width">
                                        <a href="blockchain_0.php" class="main-button main-button--gray main-button--full-width">
                                            <span>Cancel</span>
                                        </a>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <aside>
            <input type="checkbox" name="trigger" id="trigger">
            <button class="button_plus"><label for="trigger"></label></button></label>
            <div class="status_display">Delivery status: <?php echo $status[$current_status]->status ?></div>
        </aside>
    </body>
</html>