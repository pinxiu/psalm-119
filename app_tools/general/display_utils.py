def show_passage(reference, passage, flag=False, username=''):
	if flag:
		number = 'Hide Verse Number'
	else:
		number = 'Show Verse Number'
	return render_template('index.html', reference=reference, passage=passage, number=number, user=username, email=get_email(username))

def show_user_not_login():
	return render_template('index.html', error='Please log in.')