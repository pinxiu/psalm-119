def display_quiz(username):
	quiz_info = dict()
	for reference in get_flashcards(username).keys():
		quiz_info[reference] = re.subn('\n', ' ', find_passage(reference)[1].rstrip())[0]
	html_str = """

<!doctype html>
<head>
<title>Read God's Word</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
<link href="https://fonts.googleapis.com/css?family=Open+Sans|Source+Sans+Pro" rel="stylesheet">
<script language="JavaScript" type="text/javascript" src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<style>
body {
  margin: auto;
  text-align: left;
  font-weight: 300;
  font-size: 16px;
  font-family: 'Open Sans', sans-serif;
  color: #121212;
}

/* Main content */
.main {
	margin: 20px;
	margin-top: 60px; /* Add a top margin to avoid content overlay */
}

.container {
  height:120px;
  width:600px;
  margin:auto;
  margin-bottom: 30px;
  position:relative;
}

/* Add a black background color to the top navigation */
.topnav {
	background-color: #333;
	overflow: hidden;
	position: fixed; /* Set the navbar to fixed position */
	top: 0; /* Position the navbar at the top of the page */
	width: 100%; /* Full width */
	z-index:1;
}

/* Style the links inside the navigation bar */
.topnav a, input[type=button], input[type=submit], input[type=reset], button {
	float: left;
	color: #f2f2f2;
	text-align: center;
	padding: 14px 16px;
	text-decoration: none;
	font-weight: 300;
	font-size: 16px;
	font-family: 'Open Sans', sans-serif;
}

/* Change the color of links on hover */
.topnav a:hover {
	background-color: #ddd;
	color: black;
}

/* Add a color to the active/current link */
.topnav a.active, input[type=button], input[type=submit], input[type=reset], button {
	background-color: #4CAF50;
	color: white;
}
input[type=text], input[type=password], input[type=email] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
  font-weight: 300;
  font-size: 16px;
  font-family: 'Open Sans', sans-serif;
}

input[type=button], input[type=submit], input[type=reset], button {
  border: none;
  margin: 4px 2px;
  cursor: pointer;
  float: none;
}

/* Set a style for all buttons */
button {
  width: 100%;
}

/* Add a hover effect for buttons */
button:hover {
	opacity: 0.8;
}

textarea {
  white-space: pre-line;
  text-align: left;
  resize: vertical;
  overflow: hidden;
  min-height: 50px;
  max-height: 500px;
  font-weight: 300;
  font-size: 16px;
  font-family: 'Open Sans', sans-serif;
}
	/* The Modal (background) */
	.modal {
		display: none; /* Hidden by default */
		position: fixed; /* Stay in place */
		z-index: 1; /* Sit on top */
		left: 0;
		top: 0;
		width: 100%; /* Full width */
		height: 100%; /* Full height */
		overflow: auto; /* Enable scroll if needed */
		background-color: rgb(0,0,0); /* Fallback color */
		background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
		padding-top: 60px;
	}

	/* The Close Button */
	.close {
		/* Position it in the top right corner outside of the modal */
		position: relative;
		right: -375px;
		top: -5px;
		font-weight: 300;
		font-size: 16px;
		font-family: 'Open Sans', sans-serif;
		text-shadow: none;
		opacity: 1.0;
	}

	/* Close button on hover */
	.close:hover,
	.close:focus {
		color: #4CAF50;
		cursor: pointer;
	}

	/* Add Zoom Animation */
	.animate {
		-webkit-animation: animatezoom 0.6s;
		animation: animatezoom 0.6s
	}

	@-webkit-keyframes animatezoom {
		from {-webkit-transform: scale(0)} 
		to {-webkit-transform: scale(1)}
	}

	@keyframes animatezoom {
		from {transform: scale(0)} 
		to {transform: scale(1)}
	}

	.login-page {
	  width: 360px;
	  padding: 8% 0 0;
	  margin: auto;
	}
	.form {
	  position: relative;
	  z-index: 1;
	  background: #FFFFFF;
	  max-width: 360px;
	  margin: 0 auto 100px;
	  padding: 45px;
	  text-align: center;
	  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
	}
	.form input {
	  outline: 0;
	  background: #f2f2f2;
	  width: 100%;
	  border: 0;
	  margin: 0 0 15px;
	  padding: 15px;
	  box-sizing: border-box;
	}
	.form button {
	  outline: 0;
	  background: #4CAF50;
	  width: 100%;
	  border: 0;
	  padding: 15px;
	  color: #FFFFFF;
	  -webkit-transition: all 0.3 ease;
	  transition: all 0.3 ease;
	  cursor: pointer;
	}
	.form button:hover,.form button:active,.form button:focus {
	  background: #43A047;
	}

#sidebar {
	min-width: 80px;
	max-width: 80px;
	height: 100%;
	background: #567;
	color: #fff;
	transition: all 0.3s;
	position: fixed;
	z-index: 1;
	overflow: scroll;
}

/* Shrinking the sidebar from 250px to 80px and center aligining its content*/
#sidebar.active {
	min-width: 250px;
	max-width: 250px;
}

/* Toggling the sidebar header content, hide the big heading [h3] and showing the small heading [strong] and vice versa*/
#sidebar .sidebar-header h6 {
	display: none;
}
#sidebar.active .sidebar-header strong {
	display: none;
}
#sidebar.active .sidebar-header h6 {
	display: block;
}

#sidebar .sidebar-option .big {
	display: none;
}
#sidebar.active .sidebar-option .small {
	display: none;
}
#sidebar.active .sidebar-option .big {
	display: block;
}

#sidebar ul li a {
	text-align: left;
}

#sidebar.active ul li a {
	padding: 20px 10px;
	text-align: center;
	font-size: 0.85em;
}

#sidebar.active ul li a i {
	margin-right:  0;
	display: block;
	font-size: 1.8em;
	margin-bottom: 5px;
}

/* Same dropdown links padding*/
#sidebar.active ul ul a {
	padding: 10px !important;
}

/* Changing the arrow position to bottom center position, 
   translateX(50%) works with right: 50% 
   to accurately  center the arrow */
#sidebar.active .dropdown-toggle::after {
	top: auto;
	bottom: 10px;
	right: 50%;
	-webkit-transform: translateX(50%);
	-ms-transform: translateX(50%);
	transform: translateX(50%);
}
</style>
</head>
<body>

<div class="topnav">
  <a href="/"""+username+"""">Reading</a>
  <a href="/notes/"""+username+"""">Notes</a>
  <a href="/progress/"""+username+"""">Progress</a>
  <a href="/flashcards/"""+username+"""">Flashcards</a>
  <a class="active" href="/quiz/"""+username+"""">Quiz</a>
  <a href="/help/"""+username+"""">Help</a>
  <a href="/feedback/"""+username+"""">Feedback</a>"""
	html_str += """
  <input style="margin:0;float:right;" type="button" onclick="document.getElementById('login').style.display='block'" value='"""+username+"""'>
				"""
	html_str += """
</div>
				"""
	html_str += """

<div id="login" class="modal">

  <!-- Modal Content -->
  <div class="animate">
	<div class="login-page">
	  <span onclick="document.getElementById('login').style.display='none'" 
class="close" title="Close Modal">Close</span>
	  <div class="form">
		<form class="logout-form" action="/logout">
		  <p style="text-align:left;"><b>Email: </b>"""+get_email(username)+"""</p>
		  <button>Log Out</button>
		</form>
	  </div>
	</div>
  </div>
</div>

<script>
// Get the modal
var modal = document.getElementById('login');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
}
</script>
				"""

	html_str += """

<div class="main">

	<!-- Sidebar  -->
	<nav id="sidebar">
		<div align="middle" class="sidebar-header">
			<div style="margin:5px;" id="sidebarCollapse">
				<h6><i  class="fas fa-align-left"></i>&nbsp;&nbsp;
				Table of Content</h6>
				<strong><i  class="fas fa-align-left"></i>
				Table</strong>
			</div>
		</div>

		<div align="left" class="sidebar-option">
			<form id="orderStyle"">
			  <input type="radio" name="ordering" id="inorder" oninput="reorder();" checked> Sorted<br>
			  <input type="radio" name="ordering" id="random" oninput="reorder();"> Random
			</form>
		</div>

		<br>

		<ul class="list-unstyled components">
			<li class="active">
				<a href="#homeSubmenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
					Verses
				</a>
				<ul class="collapse list-unstyled" id="homeSubmenu">
				"""
	for ref in sort_verses(get_flashcards(username).keys()):
		html_str += """
						<li>
							<a href='#"""+ref+"""'>"""+ref+"""</a>
						</li>
					"""
	html_str += """
				</ul>
			</li>
		</ul>

	</nav>
<div class="container">
				"""
	counter = 0
	for reference in quiz_info:
		counter += 1
		html_str += """
	<div id='"""+reference+"""'>
		<p style="width:500px;">"""+reference+"""</p>
		<textarea cols="60" rows="5" onkeyup="setHeight('ans"""+str(counter)+"""');" id='ans"""+str(counter)+"""' type="text" oninput="checkAns('"""+str(counter)+"""')"></textarea>
		<p>
			<label id='mark"""+str(counter)+"""'>&#9997</label>
			&nbsp;&nbsp;
			<input id='case"""+str(counter)+"""' type="checkbox" checked oninput="checkAns('"""+str(counter)+"""')"> Case Sensitive
			&nbsp;&nbsp;&nbsp;
			<input id='punc"""+str(counter)+"""' type="checkbox" checked oninput="checkAns('"""+str(counter)+"""')"> Punctuation Sensitive 
		</p>
		<input id='showAns"""+str(counter)+"""' type="button" onclick="showAns('"""+str(counter)+"""')" value='Show Answer'>
		<p style="width:500px; visibility:hidden" id='key"""+str(counter)+"""'>"""+quiz_info[reference]+"""</p>
		<hr>
	</div>
					"""
	html_str += """

</div>

</div>
<script>
function checkAns(index) {
	var key = document.getElementById('key'+index).innerHTML;
	var ans = document.getElementById('ans'+index).value;
	var puncS = document.getElementById('punc'+index).checked;
	var caseS = document.getElementById('case'+index).checked;
	key = key.trim().replace(/\s+/g, " ");
	ans = ans.trim().replace(/\s+/g, " ");
	if (!puncS) {
		key = key.replace(/[^\w\s]|_/g, "");
		ans = ans.replace(/[^\w\s]|_/g, "");
	}
	if (!caseS) {
		key = key.toLowerCase();
		ans = ans.toLowerCase();
	}
	if (ans != key.substring(0, ans.length)) {
		document.getElementById('mark'+index).innerHTML = '&#10008';
	} else if (ans.length == key.length) {
		document.getElementById('mark'+index).innerHTML = '&#10004';
	} else {
		document.getElementById('mark'+index).innerHTML = '&#9997';
	}
}

function showAns(index) {
	if (document.getElementById('showAns'+index).value == 'Show Answer') {
		document.getElementById('showAns'+index).value = 'Hide Answer';
		document.getElementById('key'+index).style = "width:500px; visibility:visible";
	} else {
		document.getElementById('showAns'+index).value = 'Show Answer';
		document.getElementById('key'+index).style = "width:500px; visibility:hidden";
	}
}

function setHeight(field){
  document.getElementById(field).style.height = "106px";
  document.getElementById(field).style.height = (document.getElementById(field).scrollHeight)+'px';
}
</script>
</body>
</html>


			   """
	return html_str