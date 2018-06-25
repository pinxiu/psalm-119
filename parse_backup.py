import json

with open('backup.json') as f:
	data = json.load(f)

for user in data:
	print(user)