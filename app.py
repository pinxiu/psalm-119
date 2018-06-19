from flask import Flask, request, render_template, redirect
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search/')
@app.route('/search/<reference>')
@app.route('/search/<reference>/<flag>')
def search(reference='', flag='false'):
	if flag == 'true':
		flag = True
	else:
		flag = False
	if reference:
		reference, passage = find_passage(reference, flag)
	else:
		return render_template('index.html')
	if passage:
		return show_passage(reference, passage, flag)
	else:
		return render_template('index.html', error='Cannot find passage')

@app.route('/flashcards/')
def flash():
	return display_flash_cards()

def display_flash_cards():
	flash_cards = get_flash_cards()
	html_str = """
<!doctype html>
<head>
<title>Read God's Word</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
<link href="https://fonts.googleapis.com/css?family=Open+Sans|Source+Sans+Pro" rel="stylesheet">
<style>
	body {
	  width: 1000px;
	  margin: auto;
	  font-weight: 300;
	  font-size: 16px;
	  font-family: 'Open Sans', sans-serif;
	  color: #121212;
	}

	/* Add a black background color to the top navigation */
	.topnav {
	    background-color: #333;
	    overflow: hidden;
	}

	/* Style the links inside the navigation bar */
	.topnav a {
	    float: left;
	    color: #f2f2f2;
	    text-align: center;
	    padding: 14px 16px;
	    text-decoration: none;
	    font-size: 17px;
	}

	/* Change the color of links on hover */
	.topnav a:hover {
	    background-color: #ddd;
	    color: black;
	}

	/* Add a color to the active/current link */
	.topnav a.active {
	    background-color: #4CAF50;
	    color: white;
	}
	h1, h2, h3, h4 {
	  font-family: 'Source Sans Pro', sans-serif;
	}

	.container {
	  height:120px;
	  width:600px;
	  margin:auto;
	  position:relative;
	}

	.flip-container {
	  perspective: 1000;
	  margin: 10px;
	  float: left;
	  cursor:pointer;
	}

	  .flippable {
	    transition: 0.5s;
	    transform-style: preserve-3d;
	    position: relative;
	  }

	  .flipme {
	    transform: rotateY(180deg);
	  }
	  
	

	.flip-container, .front, .back {
	  width: 500px;
	  height: 300px;
	  text-align: center;
	  overflow-wrap: break-word;
	  overflow: scroll;
	  font-size: 40px;
	  border-radius: 10px;
	}

	.front, .back {
		color: white;
		background:#4CAF50;
		backface-visibility: hidden;
		position: absolute;
		top: 0;
		left: 0;
	}

	.front {
	  z-index: 2;
	  line-height: 280px;
	}

	.back {
	  transform: rotateY(180deg);
	  padding: 50px;
	  font-size: 18px;
	  text-align: left;
	  white-space: pre-line;
	}

</style>
<script language="JavaScript" type="text/javascript" src="https://code.jquery.com/jquery-3.3.1.min.js"></script>

</head>
<body>

<div class="topnav">
  <a href="/">Reading</a>
  <a href="/notes">Notes</a>
  <a href="/progress">Progress</a>
  <a class="active" href="/flashcards">Flash Cards</a>
  <a href="/quiz">Quiz</a>
</div>

<div class="container">
				"""
				
	html_str += show_flash_cards(flash_cards)
	html_str += """
</div>
<script>
	$(".flippable").click(function(){
	  $(this).toggleClass("flipme");
	});
</script>
</body>
</html>
				"""
	return html_str

def show_flash_cards(flash_cards):
	html_str = ""
	for reference in flash_cards:
		passage = find_passage(reference)[1]
		_, reviewed, score, times = flash_cards[reference]
		html_str += """
	<div class="flip-container" ontouchstart="this.classList.toggle('hover');">
      <div class="flippable appcon ac">
        <div class="front">"""+reference+"""</div>
        <div class="back">"""+passage+"""</div>
      </div>
  	</div>
		  """
	return html_str

@app.route('/quiz/')
def quiz():
	return display_flash_cards()

@app.route('/progress/')
def progress():
	return display_progress()

import json
import re

with open('ESV.json') as f1:
	data = json.load(f1)

with open('order.json') as f2:
	order = json.load(f2)

with open('index.json') as f3:
	book_index = json.load(f3)

with open('short_hand.json') as f4:
	short_hand = json.load(f4)

def display_progress():
	status = get_progress()
	html_str = """
<!doctype html>
<head>
<title>Read God's Word</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
<link href="https://fonts.googleapis.com/css?family=Open+Sans|Source+Sans+Pro" rel="stylesheet">
</head>
<style>
	body {
	  width: 1000px;
	  margin: auto;
	  text-align: left;
	  font-weight: 300;
	  font-size: 16px;
	  font-family: 'Open Sans', sans-serif;
	  color: #121212;
	}
	.progress {
	  white-space: pre-line;
	}
	.container {
	  padding: 10px;
	}
	.grid-container {
	  display: grid;
	  grid-template-columns: auto auto auto auto auto auto auto auto auto auto;
	}
	.grid-item {
	  padding: 2px;
	  text-align: right;
	}

	/* Add a black background color to the top navigation */
	.topnav {
	    background-color: #333;
	    overflow: hidden;
	}

	/* Style the links inside the navigation bar */
	.topnav a {
	    float: left;
	    color: #f2f2f2;
	    text-align: center;
	    padding: 14px 16px;
	    text-decoration: none;
	    font-size: 17px;
	}

	/* Change the color of links on hover */
	.topnav a:hover {
	    background-color: #ddd;
	    color: black;
	}

	/* Add a color to the active/current link */
	.topnav a.active {
	    background-color: #4CAF50;
	    color: white;
	}
	h1, h2, h3, h4 {
	  font-family: 'Source Sans Pro', sans-serif;
	}
</style>
<body>

<div class="topnav">
  <a href="/">Reading</a>
  <a href="/notes">Notes</a>
  <a class="active" href="/progress">Progress</a>
  <a href="/flashcards">Flash Cards</a>
  <a href="/quiz">Quiz</a>
</div>

<div>
				"""
				
	html_str += display(status)
	html_str += """
</div>
</body>
</html>
				"""
	return html_str

def display(status):
	result = ''
	read, total = 0, 0
	for book in sorted(status, key=lambda b: int(order[b])):
		book_status = '<div class="grid-container">'
		b_read, b_total = 0, 0
		for chapter in sorted(status[book], key=lambda c: int(c)):
			c_read = sum([1 for v in status[book][chapter].values() if v == 'true'])
			c_total = len(status[book][chapter])
			b_read += c_read
			b_total += c_total
			book_status += create_label(chapter + ': ', "%.2f%%" % (100 * c_read / c_total))
		if book == 'Psalm':
			book = 'Psalms'
		book_status = create_bar(book + ': ', "%.2f%%" % (100 * b_read / b_total)) + book_status + '</div>'
		read += b_read
		total += b_total
		result += book_status
		result += '\n\n'
	return create_bar('Total:', "%.2f%%" % (100 * read / total)) + result

def create_label(label, value):
	if value == "0.00%":
		btype = "badge badge-danger"
	elif value == "100.00%":
		btype = "badge badge-success"
	else:
		btype = "badge badge-warning"
	return """
	<div class="grid-item">
	  """+label+"""
	  <span class='"""+btype+"""'>"""+value+"""</span>
	</div>
		  """

def create_bar(label, value):
	if value == "0.00%":
		btype = "progress-bar bg-danger"
	elif value == "100.00%":
		btype = "progress-bar bg-success"
	else:
		btype = "progress-bar bg-warning"
	return """
	<div class="container">
	  <h4>"""+label+"""</h4>
	  <div class="progress">
	    <div class='"""+btype+"""'role="progressbar" aria-valuenow='"""+value[:-1]+"""' aria-valuemin="0" aria-valuemax="100" style="width:"""+value+"""">
	      <span>"""+value+""" Complete</span>
	    </div>
	  </div>
	</div>
		  """

def get_progress():
	status_dir = 'status.json'
	if not os.path.exists(status_dir):
		inventory = dict()
		for book in data:
			inventory[book] = dict()
			for chapter in data[book]:
				inventory[book][chapter] = dict()
				for verse in data[book][chapter]:
					inventory[book][chapter][verse] = 'false'
		with open(status_dir, 'w') as f2:
			f2.write(json.dumps(inventory))
	with open(status_dir) as s:
		status = json.load(s)
	return status

def get_flash_cards():
	flash_dir = 'flash.json'
	if not os.path.exists(flash_dir):
		with open(flash_dir, 'w') as fc:
			fc.write('{}\n')
	with open(flash_dir) as fc:
		flash_cards = json.load(fc)
	return flash_cards

@app.route('/notes/')
def notes():
	return render_template('notes.html', notes=get_notes())

import os
from os import listdir

def create_flash_card(reference):
	# reference, reviewed, score, visited_times
	return [reference, False, 0.0, 0]

def get_notes():
	note_dir = 'notes'
	if not os.path.exists(note_dir):
		os.makedirs(note_dir)
	notes = ''
	for file_name in os.listdir(note_dir):
		if file_name[0] == '.':
			continue
		with open(note_dir + '/' + file_name) as temp:
			notes += temp.read() + '\n\n'
	return notes

@app.route('/store/')
@app.route('/store/<reference>')
@app.route('/store/<reference>/<flag>')
def store(reference='', flag=False):
	flash_cards = get_flash_cards()
	if reference and reference not in flash_cards:
		flash_cards[reference] = create_flash_card(reference)
		with open('flash.json', 'w') as o:
			o.write(json.dumps(flash_cards))
	return redirect('/search/' + reference + '/' + flag)

@app.route('/check/')
@app.route('/check/<reference>')
def check(reference=''):
	status = get_progress()
	if reference:
		book1, chapter1, verse1, book2, chapter2, verse2 = parse(reference)
		if book2:
			if book1 == book2:
				check_book(status, book1, chapter1, verse1, chapter2, verse2)
			else:
				check_book(status, book1, chapter1=chapter1, verse1=verse1)
				for i in range(int(order[book1]) + 1, int(order[book2])):
					check_book(status, book_index[str(i)])
				check_book(status, book2, chapter2=chapter2, verse2=verse2)
		else:
			check_book(status, book1, chapter1, verse1, chapter1, verse1)
	with open('status.json', 'w') as o:
		o.write(json.dumps(status))
	return redirect('/')

def check_book(status, book, chapter1=None, verse1=None, chapter2=None, verse2=None):
	if chapter1 == None:
		chapter1 = '1'
	if chapter2 == None and verse2:
		chapter2 = chapter1
	elif chapter2 == None:
		chapter2 = max(data[book], key=lambda c: int(c))
	if chapter1 == chapter2:
		check_chapter(status, book, chapter1, verse1, verse2)
	else:
		check_chapter(status, book, chapter1, start=verse1)
		for chapter in range(int(chapter1) + 1, int(chapter2)):
			check_chapter(status, book, str(chapter))
		check_chapter(status, book, chapter2, end=verse2)
	return status

def check_chapter(status, book, chapter, start=None, end=None):
	if not start:
		start = '1'
	if not end:
		end = max(data[book][chapter], key=lambda v: int(v))
	for verse in range(int(start), int(end) + 1):
		check_verse(status, book, chapter, str(verse))
	return status

def check_verse(status, book, chapter, verse):
	status[book][chapter][verse] = 'true'
	return status

import datetime

@app.route('/submit/')
@app.route('/submit/<reference>/<note>')
@app.route('/submit/<reference>/<note>/<flag>')
def submit(reference='', note='', flag=False):
	if reference and note:
		note = reference + '\n' + note
		with open('notes/' + re.subn('\W', '_', reference + '_' + str(datetime.datetime.now())[:-7])[0] + '.txt', 'w') as f0:
			f0.write(note)
	return redirect('/search/' + reference + '/' + flag)

def show_passage(reference, passage, flag=False):
	if flag:
		number = 'Hide Verse Number'
	else:
		number = 'Show Verse Number'
	return render_template('index.html', reference=reference, passage=passage, number=number)

def find_passage(reference, flag=False):
	try:
		book1, chapter1, verse1, book2, chapter2, verse2 = parse(reference)
		passage = ''
		if book2:
			if book1 == book2:
				passage = get_book(book1, chapter1, verse1, chapter2, verse2, flag=flag)
			else:
				passage = get_book(book1, chapter1=chapter1, verse1=verse1, flag=flag)
				for i in range(int(order[book1]) + 1, int(order[book2])):
					passage += get_book(book_index[str(i)], flag=flag)
				passage += get_book(book2, chapter2=chapter2, verse2=verse2, flag=flag)
		else:
			passage = get_book(book1, chapter1, verse1, chapter1, verse1, flag=flag)
		return fixed_reference(book1, chapter1, verse1, book2, chapter2, verse2), passage
	except KeyError:
		return None, None

def fixed_reference(book1, chapter1, verse1, book2, chapter2, verse2):
	if book1 == book2:
		book2 = None
	if not book2 and chapter1 == chapter2:
		chapter2 = None
	if book1 == 'Psalm' and not chapter1:
		book1 = 'Psalms'
	if book2 == 'Psalm' and not chapter2:
		book2 = 'Psalms'
	result = book1
	if chapter1:
		result += ' ' + chapter1
	if verse1:
		result += ':' + verse1
	if book2 or chapter2 or verse2:
		result += '-'
	if book2:
		result += book2
	if chapter2:
		if book2:
			result += ' '
		result += chapter2
	if verse2:
		if chapter2:
			result += ':'
		result += verse2	
	return result

def get_book(book, chapter1=None, verse1=None, chapter2=None, verse2=None, flag=False):
	passage = ''
	if chapter1 == None:
		chapter1 = '1'
	if chapter2 == None and verse2:
		chapter2 = chapter1
	elif chapter2 == None:
		chapter2 = max(data[book], key=lambda c: int(c))
	if chapter1 == chapter2:
		passage += get_chapter(book, chapter1, verse1, verse2, flag=flag)
	else:
		passage += get_chapter(book, chapter1, start=verse1, flag=flag)
		for chapter in range(int(chapter1) + 1, int(chapter2)):
			passage += get_chapter(book, str(chapter), flag=flag)
		passage += get_chapter(book, chapter2, end=verse2, flag=flag)
	return passage + '\n'

def get_chapter(book, chapter, start=None, end=None, flag=False):
	if flag:
		passage = book + ' ' + chapter + '\n\n'
	else:
		passage = ''
	if not start:
		start = '1'
	if not end:
		end = max(data[book][chapter], key=lambda v: int(v))
	for verse in range(int(start), int(end) + 1):
		passage += get_verse(book, chapter, str(verse), flag=flag)
	return passage + '\n'

def get_verse(book, chapter, verse, flag=False):
	if flag:
		result = verse + ' '
	else:
		result = ''
	result += data[book][chapter][verse]
	result = re.subn('(?P<prefix>\w[^\w\s-])(?P<suffix>\w)', '\g<prefix> \g<suffix>', result)[0] + '\n'
	return re.subn("' s", "'s", result)[0]

def parse(reference):
	reference = fix_number(reference)
	reference = fix_signs(reference)
	m = re.match('^\s*(?P<book1>[1-3]?\s*[a-zA-Z]+)\s*(?P<chapter1>[0-9]+)?\s*:?\s*(?P<verse1>[0-9]+)?\s*(-?\s*(?P<book2>[1-3]?\s*[a-zA-Z]+)?\s*((?P<chapter2>[0-9]+)\s*:)?\s*(?P<verse2>[0-9]+)?)?', reference)
	book1, chapter1, verse1, book2, chapter2, verse2 = m.group('book1'), m.group('chapter1'), m.group('verse1'), m.group('book2'), m.group('chapter2'), m.group('verse2')
	if verse1 == None and chapter2 == None and verse2:
		chapter2 = verse2
		verse2 = None
	book1 = fix_name(book1)
	if book2 or chapter2 or verse2:
		if book2 == None:
			book2 = book1
		book2 = fix_name(book2)
	return order_fix(book1, chapter1, verse1, book2, chapter2, verse2)

def fix_number(reference):
	reference = reference.lower()
	reference = re.subn('first', '1',reference)[0]
	reference = re.subn('second', '2',reference)[0]
	reference = re.subn('third', '3',reference)[0]
	reference = re.subn('iii ', '3',reference)[0]
	reference = re.subn('ii ', '2',reference)[0]
	reference = re.subn('i ', '1',reference)[0]
	reference = re.subn('1st', '1',reference)[0]
	reference = re.subn('2nd', '2',reference)[0]
	reference = re.subn('3rd', '3',reference)[0]
	return reference

def fix_signs(reference):
	correct_ref = ''
	for c in reference:
		if c != ':' and c != '-' and c != ' ' and not ('a' <= c <= 'z') and not ('A' <= c <= 'Z') and not ('0' <= c <= '9'):
			continue
		correct_ref += c
	return correct_ref

def fix_name(book):
	m = re.match('(?P<number>[1-3])?\s*(?P<book>[a-zA-Z]+)', book)
	book_name = m.group('book')
	if 'a' <= book_name[0] <= 'z':
		book_name = book_name[0].upper() + book_name[1:]
	for i in range(len(book_name) - 1):
		if 'A' <= book_name[i+1] <= 'Z':
			book_name[i+1] = book_name[:i+1] + book_name[i+1].lower() + book_name[i+2:]
	if m.group('number'):
		book_name = m.group('number') + ' ' + book_name
	return short_hand[book_name]

def order_fix(book1, chapter1, verse1, book2, chapter2, verse2):
	if book2 and order[book1] > order[book2]:
		tempb, tempc, tempv = book2, chapter2, verse2
		book2, chapter2, verse2 = book1, chapter1, verse1
		book1, chapter1, verse1 = tempb, tempc, tempv
	if book1 == book2 and chapter1 and chapter2 and int(chapter1) > int(chapter2):
		tempc, tempv = chapter2, verse2
		chapter2, verse2 = chapter1, verse1
		chapter1, verse1 = tempc, tempv
	if book1 == book2 and chapter1 and chapter2 and int(chapter1) == int(chapter2) and verse1 and verse2 and int(verse1) > int(verse2):
		tempv = verse2
		verse2 = verse1
		verse1 = tempv
	return book1, chapter1, verse1, book2, chapter2, verse2

