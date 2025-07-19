<?php
// Vulnerable to SQL injection
$username = $_POST['username'];
$password = $_POST['password'];

$query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
$result = mysql_query($query);

if (mysql_num_rows($result) > 0) {
    echo "Login successful!";
} else {
    echo "Invalid credentials!";
}
?>
