def app_initialize_progress():
	return make_status()

#############################
# internal helper functions #
#############################

from app_tools.general.io_utils import app_upload, app_download
from app_tools.static.constants import status_file, css_string
from app_tools.static.resources import data

def get_progress(username):
	status_dir = username + '/' + status_file
	status = app_download(status_dir, make_status())
	return status

def make_status():
	inventory = dict()
	for book in data:
		inventory[book] = dict()
		for chapter in data[book]:
			inventory[book][chapter] = dict()
			for verse in data[book][chapter]:
				inventory[book][chapter][verse] = False
	return inventory

def display_progress(username):
	status = get_progress(username)
	html_str = header_string
	html_str += """
<body>



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

<div class="container">
				"""
				
	html_str += display(status)
	html_str += """
</div>

</div>

</body>
</html>
				"""
	return html_str

def display(status):
	result = ''
	read, total = 0, 0
	for book in sorted(status, key=lambda b: int(order[b])):
		book_status = '<div class="grid-container">'
		b_read, b_total = 0, 0
		for chapter in sorted(status[book], key=lambda c: int(c)):
			c_read = sum([1 for v in status[book][chapter].values() if v])
			c_total = len(status[book][chapter])
			b_read += c_read
			b_total += c_total
			book_status += create_label(chapter + ': ', "%.2f%%" % (100 * c_read / c_total))
		if book == 'Psalm':
			book = 'Psalms'
		elif book == "Song":
			book = "Song of Solomon"
		book_status = create_bar(book + ': ', "%.2f%%" % (100 * b_read / b_total)) + book_status + '</div>'
		read += b_read
		total += b_total
		result += book_status
		result += '\n\n'
	return create_bar('Total:', "%.2f%%" % (100 * read / total)) + result

def create_label(label, value):
	if value == "0.00%":
		btype = "badge badge-danger"
	elif value == "100.00%":
		btype = "badge badge-success"
	else:
		btype = "badge badge-warning"
	return """
	<div class="grid-item">
	  """+label+"""
	  <span class='"""+btype+"""'>"""+value+"""</span>
	</div>
		  """

def create_bar(label, value):
	if value == "0.00%":
		btype = "progress-bar bg-danger"
	elif value == "100.00%":
		btype = "progress-bar bg-success"
	else:
		btype = "progress-bar bg-warning"
	return """
	</div>
	<div class="container">
	  <h4>"""+label+"""</h4>
	  <div class="progress">
		<div class='"""+btype+"""'role="progressbar" aria-valuenow='"""+value[:-1]+"""' aria-valuemin="0" aria-valuemax="100" style="width:"""+value+"""">
		  <span>"""+value+""" Complete</span>
		</div>
	  </div>
		  """