import json

with open('../json/ESV.json') as f1:
	data = json.load(f1)

inventory = dict()

for book in data:
	inventory[book] = dict()
	for chapter in data[book]:
		inventory[book][chapter] = dict()
		for verse in data[book][chapter]:
			inventory[book][chapter][verse] = 'false'

with open('../json/status.json', 'w') as f2:
	f2.write(json.dumps(inventory))


