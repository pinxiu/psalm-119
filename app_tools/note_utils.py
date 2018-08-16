def display_notes(username):
	notes = get_notes(username)
	result = ''
	for timestamp in notes:
		if timestamp[0] == '.':
			continue
		result += notes[timestamp]['reference'] + '\n' + notes[timestamp]['content'] + '\n\n'
	return re.subn('<br>', '\n', result)[0]