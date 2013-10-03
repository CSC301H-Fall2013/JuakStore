<?php
$database = "amadjuak_db";; // the name of the database.
$server = "localhost";; // server to connect to.
$user = "amadjuak_team";; //mysql username to access the database with.
$pass = "csc301";; // mysql password to access the database with.
 
/* creating new mysql link */
$mysqli = new mysqli($server, $user, $pass, $database);
 
/* connecting to database */
if(mysqli_connect_errno()) {
     printf("Failed to connect to MySql: %s\n", mysqli_connect_error());
     exit();
}
 
/* change to pickme_db database */
$mysqli->select_db("users"); // select the users table ?>
