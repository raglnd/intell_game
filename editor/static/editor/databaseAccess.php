<?php
/* 
   File added by YJ
   This file is still very much in the works. Currently debugging and trying 
   to properly query the sqlite database with an ajax request from FrontEndtoJSON
   so that suggestions can be retrieved from the database and displayed browser-side	
*/
// Code created with help from http://www.tutorialspoint.com/ajax/ajax_database.htm

// Connect to database
//$dir = 'sqlite3: db.sqlite3';
//$dbh = new PDO($dir) or die("cannot open database");

// Retrieve data from query
// $charName = $_GET['name'];


// build query
$query = "SELECT name FROM editor_character ORDER BY RANDOM() LIMIT 1";

// Execute query
$result = $dbh->query($query);
echo json_encode($result); 
?>
