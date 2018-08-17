import json

prefix = "resources/dev/json/"

with open(prefix + 'ESV.json') as f1:
	data = json.load(f1)

with open(prefix + 'order.json') as f2:
	order = json.load(f2)

with open(prefix + 'index.json') as f3:
	book_index = json.load(f3)

with open(prefix + 'short_hand.json') as f4:
	short_hand = json.load(f4)