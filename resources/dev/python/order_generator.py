import json

f = open('../txt/order.txt', 'r')
o = open('../json/order.json', 'w')
o2 = open('../json/index.json', 'w')
content = dict()
inventory = dict()
counter = 1
for line in f.readlines():
	content[line[:-1]] = str(counter)
	inventory[str(counter)] = line[:-1]
	counter += 1

o.write(json.dumps(content))
o2.write(json.dumps(inventory))
o.close()
o2.close()