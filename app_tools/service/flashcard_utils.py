def app_store_flashcard(reference, username):
	return store_flashcard(reference, username)

#############################
# internal helper functions #
#############################

from app_tools.general.book_utils import app_find_passage, app_sort_references
from app_tools.general.io_utils import app_upload, app_download
from app_tools.static.constants import flashcards_file

def get_flashcards(username):
	flash_dir = username + '/' + flashcards_file
	flashcards = app_download(flash_dir)
	return flashcards

def store_flashcard(reference, username):
	flashcards = get_flashcards(username)
	if reference and reference not in flashcards:
		flashcards[reference] = create_flashcard(reference)
		app_upload(username + '/' + flashcards_file, flashcards)

def show_flashcards(flashcards, ordering):
	html_str = ""
	if ordering == "ordered":
		sorted_verses = sort_verses(flashcards.keys())
	else:
		sorted_verses = random.sample(flashcards.keys(), len(flashcards))
	for reference in sorted_verses:
		if reference[0] == '.':
			continue
		passage = find_passage(reference)[1]
		_, reviewed, score, times = flashcards[reference]
		html_str += """
	<div class="flip-container" ontouchstart="this.classList.toggle('hover');">
	  <div class="flippable appcon ac" id='"""+reference+"""'>
		<div class="front"><div class="center_p">"""+reference+"""</div></div>
		<div class="back">"""+passage+"""</div>
	  </div>
	</div>
		  """
	return html_str

def create_flashcard(reference):
	# reference, reviewed, score, visited_times
	return [reference, False, 0.0, 0]
	
def display_flashcards(username):
	flashcards = get_flashcards(username)
	html_str = """
<!doctype html>
<head>
<title>Read God's Word</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
<link href="https://fonts.googleapis.com/css?family=Open+Sans|Source+Sans+Pro" rel="stylesheet">
<script language="JavaScript" type="text/javascript" src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script defer src="https://use.fontawesome.com/releases/v5.0.13/js/solid.js" integrity="sha384-tzzSw1/Vo+0N5UhStP3bvwWPq+uvzCMfrN1fEFe+xBmv1C/AtVX5K0uZtmcHitFZ" crossorigin="anonymous"></script>
<script defer src="https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js" integrity="sha384-6OIrr52G08NpOFSZdxxz1xdNSndlD4vdcf/q2myIUVO0VsqaGHJsB0RaBE01VTOY" crossorigin="anonymous"></script>
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
		margin-top: 60px; /* Add a top margin to avoid content overlay */
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

.wrapper {
	display: flex;
	width: 100%;
	align-items: stretch;
}

	.container {
		margin: auto;
		margin-left: 60px;
		margin-bottom: 30px;
	}

	.flip-container {
	  perspective: 1000;
	  margin: 10px;
	  float: left;
	  cursor:pointer;
	}

	  .flippable {
		transition: 0.5s;
		transform-style: preserve-3d;
		position: relative;
	  }

	  .flipme {
		transform: rotateY(180deg);
	  }
	  
	

	.flip-container, .front, .back {
	  width: 500px;
	  height: 300px;
	  text-align: center;
	  overflow-wrap: break-word;
	  overflow: scroll;
	  font-size: 40px;
	  border-radius: 10px;
	}

	.front, .back {
		color: white;
		background:#4CAF50;
		backface-visibility: hidden;
		position: absolute;
		top: 0;
		left: 0;
	}

	.front {
	  z-index: 2;
	  line-height: 280px;
	}

	.center_p {
	  line-height: 1.5;
	  display: inline-block;
	  vertical-align: middle;
	}

	.back {
	  transform: rotateY(180deg);
	  padding: 50px;
	  font-size: 18px;
	  text-align: left;
	  white-space: pre-line;
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
		right: -55px;
		top: -25px;
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
	min-width: 100px;
	max-width: 100px;
	height: 100%;
	background: #121212;
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
	font-size: 0.85em;
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
  <a class="active" href="/flashcards/"""+username+"""">Flashcards</a>
  <a href="/quiz/"""+username+"""">Quiz</a>
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

<div class="wrapper">

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

		<div class="sidebar-option" style="font-size:14px;margin-left:5px;">
			<form id="orderStyle"">
			  <input type="radio" name="ordering" id="inorder" oninput="reorder();" checked> Sorted &nbsp &nbsp
			  <input type="radio" name="ordering" id="random" oninput="reorder();"> Random
			</form>
		</div>

		<ul class="list-unstyled components" style="font-size:14px;margin-left:5px;">
			<li class="active">
				<ul class="list-unstyled" id="allLinks">
				"""
	inventory = book_sort(flashcards)
	for book in sorted(inventory, lambda x: order[x]):
		html_str += """
						<li>
							<a style="color:white;" href='#"""+book+"""' data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
								"""+book+"""
							</a>
							<ul class="collapse list-unstyled" id='"""+book+"""'>
					"""
		for chapter in sorted(inventory[book]):
			html_str += """
								<li>
									<a style="color:white;margin-left:10px;" href='#"""+book + str(chapter)+"""' data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
										ch. """+str(chapter)+"""
									</a>
									<ul class="collapse list-unstyled" id='"""+book + str(chapter)+"""'>
						"""
			for verse in sorted(inventory[book][chapter]):
				reference = inventory[book][chapter][verse]
				html_str += """
										<li>
											<a style="color:white;margin-left:20px;" href='#"""+reference+"""'>
												"""+re.subn(book + ' ', '', reference)[0]+"""
											</a>
										</li>
							"""
			html_str += """
									</ul>
								</li>
						"""
		html_str += """
							</ul>
						</li>
					"""
	html_str += """
				</ul>
			</li>
		</ul>

	</nav>

	<div id="content">
		<div class="container">
				<div id="ordered_cards">
				"""
				
	html_str += show_flashcards(flashcards, "ordered")
	html_str += """
				</div>
				<div id="random_cards">
				"""
				
	html_str += show_flashcards(flashcards, "random")
	html_str += """
				</div>
		</div>
	</div>
</div>

</div>

	<!-- jQuery CDN - Slim version (=without AJAX) -->
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	<!-- Popper.JS -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
	<!-- Bootstrap JS -->
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>

<script type="text/javascript">
	$(".flippable").click(function(){
	  $(this).toggleClass("flipme");
	});

function reorder() {
	if (document.getElementById('inorder').checked) {
		document.getElementById('ordered_cards').style = "display:block;";
		document.getElementById('random_cards').style = "display:none;";
	}
}

$(document).ready(function () {

	$('#sidebarCollapse').on('click', function () {
		$('#sidebar').toggleClass('active');
	});

});
</script>
</body>
</html>
				"""
	return html_str