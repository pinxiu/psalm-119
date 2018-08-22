def app_get_css_string():
	return css_string
def app_get_header_string():
	return header_string
def app_get_top_nav(section, username, email):
	return topnav(section, username, email)
def app_initialize_progress():
	return make_status()

app_users_file = 'users.json'
app_status_file = "status.json"
app_notes_file = "notes.json"
app_flashcards_file = "flash.json"
app_feedback_file = "feedback.json"

#############################
# internal helper functions #
#############################

css_string = """
<style>
	body {
	  margin: auto;
	  text-align: left;
	  font-weight: 300;
	  font-size: 16px;
	  font-family: 'Open Sans', sans-serif;
	  color: #121212;
	}
	.grid-container {
	  display: grid;
	  grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
	}
	.grid-item {
	  padding: 2px;
	  text-align: right;
	}

	/* Main content */
	.main {
		margin: 20px;
		margin-top: 60px; /* Add a top margin to avoid content overlay */
	}

	.container {
		margin: auto;
		margin-bottom: 30px;
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

	/* Extra style for the cancel button (red) */
	.cancelbtn {
		width: auto;
		padding: 10px 18px;
		background-color: #f44336;
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
	.form .message {
	  margin: 15px 0 0;
	  color: #b3b3b3;
	  font-size: 12px;
	}
	.form .message a {
	  color: #4CAF50;
	  text-decoration: none;
	}
	.form .register-form {
	  display: none;
	}
	.form .reset-form {
	  display: none;
	}
</style>
			 """

header_string = """
<!doctype html>
<head>
<title>Read God's Word</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
<link href="https://fonts.googleapis.com/css?family=Open+Sans|Source+Sans+Pro" rel="stylesheet">
<script language="JavaScript" type="text/javascript" src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
				""" \
				+ css_string + \
				"""
</head>
			 	"""

sections = {'':'Reading', 'notes':'Notes', 'progress':'Progress', 'flashcards':'Flashcards', \
'quiz':'Quiz', 'help':'Help', 'feedback':'Feedback'}

def top_nav(section, username, email):
	html_str = """
<div class="topnav">
			   """
	for addr in sections:
		if addr == section:
			active_attribute = 'class="active" '
		else:
			active_attribute = ''
		html_str += """
  <a """+active_attribute+"href='/"+section+"/"+username+"'>"+sections[addr]+"""</a>
			   		"""
	html_str += """
  <input style="margin:0;float:right;" type="button" onclick="document.getElementById('login').style.display='block'" value='"""+username+"""'>
				"""

	html_str += """
</div>
				"""
	if username:
		html_str += """

<div id="login" class="modal">

  <!-- Modal Content -->
  <div class="animate">
	<div class="login-page">
	  <span onclick="document.getElementById('login').style.display='none'" 
class="close" title="Close Modal">Close</span>
	  <div class="form">
		<form class="logout-form" action="/logout">
		  <p style="text-align:left;"><b>Email: </b>"""+email+"""</p>
		  <button>Log Out</button>
		</form>
	  </div>
	</div>
  </div>
</div>
					"""
	else:
		html_str += """
<div id="login" class="modal">
  <!-- Modal Content -->
  <div class="animate">
    <div class="login-page">
      <span onclick="document.getElementById('login').style.display='none'" 
class="close" title="Close Modal">Close</span>
      <div class="form">
        <form class="register-form" action="/register">
          <input type="text" name="reguname" placeholder="username"/>
          <input type="password" name="regpsw" placeholder="password"/>
          <input type="email" name="regemail" placeholder="email address"/>
          <button>Register</button>
          <p class="message">Already registered? <a id="a3" href="#">Log In</a></p>
        </form>
        <form class="reset-form" action="/reset">
          <input type="text" name="resuname" placeholder="username"/>
          <input type="email" name="resemail" placeholder="email address"/>
          <input type="password" name="respsw" placeholder="new password"/>
          <button>Reset Password</button>
          <p class="message">Try again? <a id="a4" href="#">Log In</a></p>
        </form>
        <form class="login-form" action="/login">
          <input type="text" name="loguname" placeholder="username"/>
          <input type="password" name="logpsw" placeholder="password"/>
          <button>Log In</button>
          <p class="message">Not registered? <a id="a1" href="#">Create an account</a></p>
          <p class="message">Forgot password? <a id="a2" href="#">Reset password</a></p>
        </form>
      </div>
    </div>
  </div>
</div>

<script type="text/javascript">
$('#a1').click(function(){
   $('.login-form').hide();
   $('.reset-form').hide();
   $('.register-form').show();
});
$('#a2').click(function(){
   $('.login-form').hide();
   $('.reset-form').show();
   $('.register-form').hide();
});
$('#a3').click(function(){
   $('.login-form').show();
   $('.reset-form').hide();
   $('.register-form').hide();
});
$('#a4').click(function(){
   $('.login-form').show();
   $('.reset-form').hide();
   $('.register-form').hide();
});
</script>
					"""
	return html_str

def make_status():
	inventory = dict()
	for book in data:
		inventory[book] = dict()
		for chapter in data[book]:
			inventory[book][chapter] = dict()
			for verse in data[book][chapter]:
				inventory[book][chapter][verse] = False
	return inventory
