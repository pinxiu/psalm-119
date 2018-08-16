import json
import sys
import os

prefix = "resources/web/backup"

if not os.path.exists(prefix):
	os.makedirs(prefix)

for file_name in sys.argv[1:]:

	with open(prefix + '/json/' + file_name + '.json') as f:
		data = json.load(f)

	file_name = prefix + '/' + file_name

	if not os.path.exists(file_name):
		os.makedirs(file_name)
	user_info = dict()

	for user in data:
		if not os.path.exists(file_name + '/' + user):
			os.makedirs(file_name + '/' + user)
		user_info[user] = dict()
		user_info[user]['secret'] = data[user]['secret']
		user_info[user]['email'] = data[user]['email']
		for file_type in ['flash', 'notes', 'status']:
			with open(file_name + '/' + user + '/' + file_type + '.json', 'w') as o:
				o.write(json.dumps(data[user][file_type + '.json']))
	with open(file_name + '/users.json', 'w') as u:
		u.write(json.dumps(user_info))
