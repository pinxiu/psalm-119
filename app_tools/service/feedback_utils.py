def app_submit_feedback(note, username):
	return submit_feedback(note, username)

#############################
# internal helper functions #
#############################

from app_tools.general.io_utils import app_upload, app_download

def get_feedback():
	feed_dir = 'feedback.json'
	feed = download(feed_dir)
	return feed

def submit_feedback(note, username):
	if note:
		feed_dir = 'feedback.json'
		feed = download(feed_dir)
		result = dict()
		result['username'] = username
		result['content'] = note
		feed[str(datetime.datetime.now())] = result
		upload(feed_dir, feed)