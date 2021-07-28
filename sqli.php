<html>
	<head>
		<style>
			table, th, td {
			  border: 1px solid black;
			  border-collapse: collapse;
			}
		</style>
	</head>
	<body>
		<h1>Attacks</h1>
		<ul>
			<li>
				<a href="rce.php">Command Injection</a>
			</li>
			<li>
				<a href="sqli.php">XSS</a>
			</li>
			<li>
				<a href="sqli.php">SQL Injection</a>
			</li>
		</ul>
		<br><br>
		<?php
			$servername = "127.0.0.1";
			$username = "root";
			$password = "password";
			$dbname = "assignment2";
			
			$name = $_GET[name];
		?>
		<div>
			<h1>User Information</h1>
		</div>
		<div>
			<form method="get" action="/sqli.php">
				<label for="fname">Enter search:</label>
	  			<input type="text" id="name" name="name" value="<?php echo (isset($name))?$name:''; ?>"><br><br>
				<input type="submit" value="Submit"/>
			</form>
			<br><br>
			<?php
				$conn = new mysqli($servername, $username, $password, $dbname);
				$sql = "SELECT personid,firstname,lastname FROM users";
				if(isset($name)) {
					echo "Showing results for: " . $name;
					$sql = "SELECT personid,firstname,lastname FROM users where (firstname LIKE '%" . $name . "%') OR (lastname LIKE '%" . $name . "%')";
					echo "<br>" . $sql;
				}
			?>
			<table style="width:30%">
				<tr>
					<th>Id</th>
					<th>First Name</th>
					<th>Last Name</th>
				</tr>
			
			<?php
				$result = mysqli_query($conn, $sql) or die(mysqli_error($conn));
				if (mysqli_num_rows($result) > 0) {
					// output data of each row
					
					while($row = mysqli_fetch_assoc($result)) {
						echo "<tr><td>" . $row["personid"]. "</td><td>" . $row["firstname"]. "</td><td>" . $row["lastname"]. "</td></tr>";
					}
				}
				else {
					echo "<br><br>" . mysql_error();
				}
			?>
			</table>
		</div>
	</body>
</html>
