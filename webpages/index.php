<HTML>
<head>
	<title>Dark side/none HPOC Staging workshop script via container</title>
	<link rel="stylesheet" href="/css/bootstrap.min.css">
	<link rel="stylesheet" href="/css/bootstrap-theme.min.css">
	<link rel="stylesheet" href="/css/base.css">
</head>
<body style="color: rgb(0, 0, 0); background: linear-gradient(rgba(64, 64, 64, 0.75), rgba(64, 64, 64, 0.75)) 0% 0% / 100% 100%, url('/img/background-min.jpg');">
	<img src="/img/login_logo.png" style="width:540px; height: auto;">
<BR>
<div class="prettyDiv">
<?php
	# Some needed parameters
	$word_start = 'WORKSHOPS=(\\';
	$word_stop = ') #';
	$count=0;
	$cluster_file='cluster.txt';
	$images_loc='/images';

	# Read the workshops from the stage_workshop.sh file so we have the same values from there
	$file = file('/opt/stageworkshop/stage_workshop.sh');
	for ($i = 1; $i < count($file); $i++) {
		if (strpos($file[$i],$word_start) === 0){ # 0 means we have found the string
			$i++;
			while (strpos($file[$i],$word_stop) !== 0){ # Until we have found the Stop string, show the lines
				$workshop_ar[$count]=trim(substr($file[$i],0,-3),"\"");
				$count++;
				$i++;
			}
		}
	}

	# Do we have a variable for the workshop??? If yes, then show the result and wait for a go!
	if (!isset($_POST["workshop"])){
		echo "<H3>This website controls the settings for the stageworkshop container</H3>";
		echo "<P> The following provides the webshops that are available in this script</P>";
		echo "<FORM action=\"index.php\" method=\"POST\">\n";
		echo "Which of the following workshops do you want to run?<P>\n";
		for ($i=0;$i<sizeof($workshop_ar);$i++){
			$val_count=intval($i)+1;
			echo "<INPUT TYPE=\"radio\" NAME=\"workshop\" VALUE=".$val_count.">".$workshop_ar[$i]."<BR>\n";
		}
		echo "<center><input type=\"submit\" VALUE=\"Submit\"></center><br>\n";
		echo "</FORM>\n";
	}elseif (!isset($_POST["GO"])){ # We are not yet good to go!
		$workshop_nr=intval($_POST["workshop"])-1;
		# Show some information before the script runs
		echo "<center>You have selected the workshop: <BR><B>".$workshop_ar[$workshop_nr]."</B><P>\n";
		echo "<P><h3>Checking needed parameters...</h3>\n";
		if (file_exists($images_loc."/".$cluster_file)){
			echo "<H3><font color=\"green\"><B>We have found the cluster.txt file.</B></center></font></H3>\n";
			echo "The following command will run: <B>bash stage_workshop.sh -w ".$_POST["workshop"]." -f /images/cluster.txt</B><P>\n";
			echo "<FORM action=\"index.php\" method=\"POST\">\n";
			echo "<INPUT TYPE=\"HIDDEN\" NAME=\"GO\" VALUE=\"GO\">\n";
			echo "<INPUT TYPE=\"HIDDEN\" NAME=\"workshop\" VALUE=\"".$_POST["workshop"]."\">\n";
			echo "<center><input type=\"submit\" VALUE=\"Start the script\"></center><br>\n";
			echo "</FORM>\n";
		}else{
			echo "<FONT COLOR=\"red\"><B>We haven't found the cluster.txt file!!!! Please <A href=\"index.php\">restart the webpage</a> and make sure the file exists</B></font><br>\n";
		}
		
	}else{
		echo "<H2>Running the script....</H2>\n";
		echo "Firing the patch script <B>stage_workshop.sh -w ".$_POST["workshop"]." -f ".$images_loc."/".$cluster_file." in the container</B><BR>\n";
		$start_script='echo "cd /opt/stageworkshop/" > /tmp/stage_script.sh && sudo chmod +x /tmp/stage_script.sh 2>&1';
		echo nl2br(shell_exec($start_script));
		$start_script="echo \"./stage_workshop.sh -w \"".$_POST["workshop"]."\" -f \"".$images_loc."\"/\"".$cluster_file." >> /tmp/stage_script.sh 2>&1";
		echo nl2br(shell_exec($start_script));
	    echo nl2br(shell_exec('tail -f /var/log/nginx/access.log 2>&1'));
		echo "<PRE>$output</pre>";
		#echo nl2br(shell_exec('sudo bash /tmp/stage_script.sh 2>&1'));
;	}
?>
</div>
</body>
</HTML>