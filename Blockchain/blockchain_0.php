<?php 
$json = file_get_contents('orders.json');
$status = json_decode($json);
$json_2 = file_get_contents('coffee.json');
$coffee = json_decode($json_2);
$current_status = 1;
?>

<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Coffeechain</title>
        <link rel="icon" type="image/png" href="https://cdn-icons-png.flaticon.com/512/2091/2091665.png">
        <link rel="stylesheet" href="blockchain_0.css">
    </head>
    <body>
        <header>
            <div class="logobox">
                <img class="icon" src="https://cdn-icons-png.flaticon.com/512/2091/2091665.png">
                <a class="logo" href="#">Coffeechain</a>
            </div>
            <nav>
                <ul class="nav-links">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Our products</a></li>
                    <li><a href="#">About us</a></li>
                </ul>
            </nav>
        </header>
        
        <main class="products-main">
            <form class="products-container" action='./blockchain_1.php' method='post'>
                <?php 
                foreach($coffee as $item) {
                    echo "<div class='product' style='background-image: url($item->image);'>";
                    echo "<input type='submit' name='$item->id' value='$item->title'>";
                    // echo "<h4>$item->title</h4>";
                    echo "<p>Price: $item->price\$</p>";
                    echo "<p>$item->description</p>";
                    echo "</div>";
                }
                ?>
            </div>
        </main>

        <footer>
            <div class="upperfooter">
                <div class="footer-column">
                    <h1>About</h1>
                    <p>Coffeechain is a fictional coffee shop created for the purpose of completing a Blockchain midterm work.</p>
                </div>
                <div class="footer-column">
                    <h1>Quick Links</h1>
                    <ul>
                        <li><a href="#">Home</a></li>
                        <li><a href="#">Our products</a></li>
                        <li><a href="#">About us</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h1>Contacts</h1>
                    <ul>
                        <li><p>Email: coffeechain@gmail.com</p></li>
                        <li><p>Phone: +7 (777) 777 7777</p></li>
                    </ul>
                </div>
            </div>
            <div class="lowerfooter">
                <p>Copyright © 2022 All Rights Reserved by Coffeechain</p>
            </div>
        </footer>
    </body>
</html>