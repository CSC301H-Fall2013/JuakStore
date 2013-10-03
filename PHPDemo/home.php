<?php
     // getting daabase connection 
     if (!file_exists('config.php')) {
          echo 'Error. Database file does not exist.';
     } else {
          require_once('config.php');
     }
 
 	// checking for session creation
     if (!isset($_SESSION)) {
          session_start();
     }
 
 	// checking if we're logged in
     if(!isset($_SESSION['loggedin']) && $_SESSION['loggedin']!='yes'){
          // not logged in
          header("location: index.php");
          exit();
     } else {
          $_SESSION['loggedin'] = 'yes';
     }
 
?>
 
 <!-- the html for the page -->
<!doctype html>
     <html>
     <head>
          <title>Home Page</title>
     </head>
     <body>
 
     <h1>Home page</h1>
     <p>Congratulations! You have successfully logged in as <?php echo $_SESSION['username'] ?></p>
     <p>Would you like to <a href="logout.php">log out</a>?</p>
     </body>
 </html>