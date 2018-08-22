def app_update_progress(username, reference):
	return update_progress(username, reference)
def app_display_progress(username):
	return display_progress(username)

#############################
# internal helper functions #
#############################

from app_tools.general.book_utils import app_check_passage
from app_tools.general.io_utils import app_upload, app_download
from app_tools.general.user_utils import app_get_email
from app_tools.static.constants import app_status_file, app_get_header_string, \
app_initialize_progress, app_get_top_nav
from app_tools.static.resources import app_book_order

def get_progress(username):
	status_dir = username + '/' + status_file
	status = app_download(status_dir, app_initialize_progress())
	return status

def upload_progress(username, status):
	status_dir = username + '/' + status_file
	status = app_upload(status_dir, status)

def update_progress(username, reference):
	status = get_progress(username)
	app_check_passage(status, reference)
	upload_progress(username, status)

def display_progress(username):
	status = get_progress(username)
	html_str = app_get_header_string()
	html_str += app_get_top_nav('progress', username, app_get_email(username))
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