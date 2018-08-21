def app_check_passage(reference):
	return check_passage(reference)

def app_find_passage(reference, showVerseNumber=False):
	return find_passage(reference, showVerseNumber)

def app_parse_reference(reference):
	return parse_reference(reference)

def app_display_reference(reference):
	return display_reference(reference)

def app_sort_references(references, flatten=True):
	return sort_references(references, flatten)

#############################
# internal helper functions #
#############################

from app_tools.service.progress_utils import app_get_progress, app_update_progress
from app_tools.static.resources import *

import re

# checking passage

def check_verse(status, book, chapter, verse):
	status[book][chapter][verse] = True
	return status

def check_chapter(status, book, chapter, start=None, end=None):
	if not start:
		start = '1'
	if not end:
		end = max(data[book][chapter], key=lambda v: int(v))
	for verse in range(int(start), int(end) + 1):
		check_verse(status, book, chapter, str(verse))
	return status

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

def check_passage(reference):
	status = app_get_progress(username)
	book1, chapter1, verse1, book2, chapter2, verse2 = parse_reference(reference)
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
	app_update_progress(username , status)

# finding passage

def get_verse(book, chapter, verse, flag=False):
	if flag:
		result = verse + ' '
	else:
		result = ''
	result += data[book][chapter][verse]
	result = re.subn('(?P<prefix>\w[^\w\s-])(?P<suffix>\w)', '\g<prefix> \g<suffix>', result)[0] + '\n'
	return re.subn("' s", "'s", result)[0]

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

def find_passage(reference, flag=False):
	try:
		book1, chapter1, verse1, book2, chapter2, verse2 = parse_reference(reference)
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
		return passage
	except KeyError:
		return None

# parsing reference

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

def fix_space(reference):
	reference = re.subn('the revelation', 'revelation',reference)[0]
	reference = re.subn('song of solomon', 'song',reference)[0]
	reference = re.subn('song of songs', 'song',reference)[0]
	reference = re.subn('canticle of canticles ', 'song',reference)[0]
	return reference

def fix_signs(reference):
	correct_ref = ''
	for c in reference:
		if c != ':' and c != '-' and c != ' ' and not ('a' <= c <= 'z') and not ('0' <= c <= '9'):
			continue
		correct_ref += c
	return correct_ref

def fix_name(book):
	m = re.match('(?P<number>[1-3])?\s*(?P<book>[a-zA-Z]+)', book)
	book_name = m.group('book')
	book_name = book_name[0].upper() + book_name[1:]
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

def parse_reference(reference):
	reference = fix_number(reference)
	reference = fix_space(reference)
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

# displaying reference
def display_reference(reference):
	book1, chapter1, verse1, book2, chapter2, verse2 = parse_reference(reference)
	return fixed_reference(book1, chapter1, verse1, book2, chapter2, verse2)

def fixed_reference(book1, chapter1, verse1, book2, chapter2, verse2):
	if book1 == book2:
		book2 = None
	if not book2 and chapter1 == chapter2:
		chapter2 = None
	if book1 == 'Psalm' and not chapter1:
		book1 = 'Psalms'
	if book2 == 'Psalm' and not chapter2:
		book2 = 'Psalms'
	if book1 == 'Song':
		book1 = 'Song of Solomon'
	if book2 == 'Song':
		book2 = 'Song of Solomon'
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

# sorting references

def get_weight(reference):
	book1, chapter1, verse1, book2, chapter2, verse2 = parse_reference(reference)
	return (int(order[book1]) * 1000 + int(chapter1)) * 1000 + int(verse1)

def sort_references(references, flag):
	if flag:
		return sort_verses(references)
	else:
		return book_sort(references)

def sort_verses(references):
	return sorted(references, key=lambda v: get_weight(v))

def book_sort(references):
	inventory = dict()
	for reference in references:
		book, chapter, verse, _1, _2, _3 = parse_reference(reference)
		chapter = int(chapter)
		verse = int(verse)
		if book not in inventory:
			inventory[book] = dict()
		if chapter not in inventory[book]:
			inventory[book][chapter] = dict()
		inventory[book][chapter][verse] = reference
	return inventory




	