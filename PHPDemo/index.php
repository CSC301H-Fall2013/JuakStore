<?php
 	// database file
     include("config.php");
 
 	// checking current session 
     if (!isset($_SESSION)) {
          session_start();
     }
 
     if(isset($_SESSION['loggedin']) && $_SESSION['loggedin']=='yes'){
          // logged in
          header("location: home.php");
          exit();
     }
 
     /* check to see if user attempted logging in */
     if($_GET["atmpt"] != NULL){
          if($_GET["atmpt"] == 2){
          // forgotten password
          $error .= "Did you forget your password?<br>";
     }
 
     /* get username and password */
     $username = $_POST["username"];
     $password = $_POST["password"];
 
     /* MySQL Injection prevention */
     $username = mysqli_real_escape_string($mysqli, stripslashes($username));
     $password = mysqli_real_escape_string($mysqli, stripslashes($password));
     
     /* check for user in database */
     $query = "SELECT * FROM Users WHERE username = '$username' AND password = '$password'"; // replace "users" with your table name
     $result = mysqli_query($mysqli, $query);
     $count = $result->num_rows;
     if($count > 0){
          //successfully logged in
          $_SESSION['username']=$username;
          $_SESSION['loggedin']='yes';
          header("location:home.php");
          exit();
     } else {
          // Login Failed
          $error .=  "Wrong Username or Password";
          $_SESSION['loggedin']='no';
          $atmpt = 2;
     }
} else {
     $atmpt = 1;
}
 
?>
 
 
<!doctype html>
<html>
     <head>
          <title>Log In</title>
     </head>
     <body>
 
     <h1>Log In</h1>
 
     <p>Enter your details below to log in to your account.</p>
 
     <span><?php echo $error ?></span>
 
     <form action="index.php?atmpt=1" method="post">
     <table>
          <tr>
               <td>Username</td>
               <td><input type="text" name="username"></td>
          </tr>
          <tr>
               <td>Password</td>
               <td><input type="password" name="password"></td>
          </tr>
          <tr>
               <td colspan="2"><input type="submit" value="Log In"></td>
          </tr>
     </table>
     </form>
 
     </body>
</html>
 