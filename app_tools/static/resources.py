import json

prefix = "resources/dev/json/"

with open(prefix + 'ESV.json') as f1:
	app_esv_content = json.load(f1)

with open(prefix + 'index.json') as f3:
	app_book_index = json.load(f3)

with open(prefix + 'order.json') as f2:
	app_book_order = json.load(f2)

with open(prefix + 'short_hand.json') as f4:
	app_book_shorthand = json.load(f4)