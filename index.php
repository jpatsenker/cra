<!DOCTYPE html>
<?php parse_ini_file("php.ini"); ?>

<html>

	<head>
		<title>
			
			CRAP

		</title>
	</head>

	<body>

		<form name="download" action="results.php" method="POST" enctype="multipart/form-data">
                
            		<div id="download_area">
               			<p><b>FASTA</b></p>
                		<input type="file" name="fastaseq">
                		<p><b>EMAIL</b></p>
                		<textarea name="email"></textarea>
                		<p></p>
                		<input type="submit"/>
            		</div>
        	</form>

	</body>





</html>
