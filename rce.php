<html>
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
			$ip = $_GET['ip'];
		?>
		<div>
			<h1>Ping Test</h1>
		</div>
		<div>
			<form method="get" action="/rce.php">
				<label for="fname">Enter IP address or Domain name:</label>
	  			<input type="text" id="ip" name="ip" value="<?php echo (isset($ip))?$ip:''; ?>"><br><br>
				<input type="submit" value="Ping"/>
			</form>
			<br><br>
			<?php
				$output = shell_exec("ping -c 4 " . $ip);
				echo "<pre>$output</pre>";
			?>
		</div>
	</body>
</html>
