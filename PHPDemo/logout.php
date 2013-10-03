<?php
 	//log-out page
     session_start();
     session_destroy();
     header("location:index.php");
     exit();
 
?>