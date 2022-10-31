<?php 
$json = file_get_contents('orders.json');
$status = json_decode($json);
$json_2 = file_get_contents('coffee.json');
$coffee = json_decode($json_2);
$current_status = 1;
$id = $_POST["id"];
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
                            <div class="main-card__header">
                                <h2 class="main-card__title">Order Summary</h2>
                                <p class="main-card__description">To finalize the order, check the information below</p>
                            </div>
                            <div class="main-card__content">
                                <div class="input-field" style="margin-bottom: 10px;">
                                    <span style="font-weight: bold;">Product name: <?php echo $coffee[$id]->title ?></span>
                                </div>
                                <div class="input-field" style="margin-bottom: 10px;">
                                    <span style="font-weight: bold;">Product quantity: <?php echo $_POST["quantity"] ?></span>
                                </div>
                                <div class="input-field" style="margin-bottom: 10px;">
                                    <span style="font-weight: bold;">Total price: <?php echo (($coffee[$id]->price) * $_POST["quantity"]) ?></span>
                                </div>
                                <div class="input-field" style="margin-bottom: 10px;">
                                    <span style="font-weight: bold;">Delivery start date: <?php echo $_POST["startdate"] ?></span>
                                </div>
                                <div class="input-field">
                                    <span style="font-weight: bold;">Delivery end date: <?php echo $_POST["enddate"] ?></span>
                                </div>
                                <div class="need_help">
                                    Need help?
                                </div>
                            </div>
                            <div class="main-card__footer">
                                <div class="main-card__bottom-btn">
                                    <button href="#" class="main-button main-button--black main-button--full-width">
                                        <span>Continue</span>
                                    </button>
                                    <a href="blockchain_0.php" class="main-button main-button--gray main-button--full-width">
                                        <span>Cancel</span>
                                    </a>
                                </div>
                            </div>
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