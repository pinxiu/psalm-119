import json

short_hand = dict()
book = ''

book_list = open('../txt/order.txt').readlines()

src = open('../txt/sh.txt')
for line in src.readlines():
	if line in book_list:
		book = line
	short_hand[line[:-1]] = book[:-1]
src.close()

with open('../json/short_hand.json', 'w') as f:
	f.write(json.dumps(short_hand))


