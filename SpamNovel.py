
'''
SPAM NOVEL
Jeff Thompson | 2014 | www.jeffreythompson.org

'''

import Markov, random, re

comments_file =			'Comments.txt'
authors_file = 			'Authors.txt'
num_words_in_novel =	50000
chapter = 				1

chance_chapter = 		0.02
chance_paragraph = 		0.01
chance_period = 		0.1
chance_question = 		0.001

# other variables (set later)
capitalize = 			True
in_dialog = 			False
chapter = 				1
add_dialog_quotes = 	True

# words for formatting sentences
pronouns = 				'(he|she|it)'
pronouns_upper = 		'(He|She|It)'
said = 					'(said|whispered|yelled|commanded|urged|plead|muttered)'
asked = 				'(asked|queried|inquired|demanded|begged)'

# not really all articles, but basically words we don't want to end a sentence with
articles = 				[ 'a', 'an', 'the', 'and', 'or', 'if', 'of', 'by', 'as' ]

# words to capitalize - list in lowercase! (could include names, places, etc)
words_to_capitalize = 	[ 'i' ]

# list of punctuation marks to look for
punctuation = 			[ '.', ',', '?', '!' ]


print 'SPAM NOVEL'

# load markov chain
with open(comments_file) as f:
	print '- parsing file (may take a while)...'
	markov = Markov.Markov(f)


# generate text
print '- generating output...'
book = ''

word_count = 0
while word_count < num_words_in_novel:
	markov_output = markov.generate_markov_text(size=1000)	# generate long set of words, will be trimmed
	words = markov_output.split(' ')
	
	for word in words:
		if capitalize:
			word = word.title()
			capitalize = False
		
		# randomly break sentence
		if random.random() < chance_period and word.lower() not in articles:
			word += '.'
			capitalize = True
			continue
		elif random.random() < chance_question and word.lower() not in articles:
			word += '?'
			capitalize = True
			continue
		book += word + ' '

		# random new paragraph and chapter
		if random.random() < chance_paragraph and word.lower() not in articles:
			book += '.\n\n'								# be sure to add a period first
			if random.random() < chance_chapter:		# random chapter
				chapter += 1
				book += '\nCHAPTER ' + str(chapter)
				book += '\n\n'
			capitalize = True
			continue

		# update word count
		word_count += 1
		if word_count > num_words_in_novel:
			break


# run general text cleanup
print '- cleaning up the text...'

# add a period at the end
if book[:-2] not in punctuation:
	book += '.'

# clean up any weirdness (easier than fixing in the code above... a hack, I know)
book = re.sub(r',+\.+', '.', book)						# , followed by .
book = re.sub(r'\?+\.+', '?', book)						# ? followed by .

book = re.sub(r'\s+\.+', '.', book)						# space before .
book = re.sub(r'\s+,+', ',', book)						# ditto ,
book = re.sub(r'\s+;+', ';', book)						# ditto ;
book = re.sub(r'\s+;+', ':', book)						# ditto :

book = re.sub(r',{2,}', ', ', book)						# more than 1 ,
book = re.sub(r'\.{2,}', '.', book)						# ditto .
book = re.sub(r'[^\S\r\n]{2,}', ' ', book)				# 2 or more spaces (ignore \n and \r)

# wow, super ugly: remove extra space at the start of paragraphs and capitalize as needed
book = re.sub(r'\n.*?(\b[a-zA-Z])', lambda pat: '\n' + pat.group(1).upper(), book)

# also ugly: make sure all sentences are capitalized (may be wrong after some of the regex above...)
book = re.sub(r'(\.|\?) ([a-z])', lambda pat: pat.group(1) + ' ' + pat.group(2).upper(), book)

# fix oddly capitalized letters after apostrophes (catches instances of things like he'Ll too)
book = re.sub(r'\'([A-Z].*?)\b', lambda pat: '\'' + pat.group(1).lower(), book)

# fix any missing end-of-paragraph periods
book = re.sub(r'(\b[^\.]\n+)', r'.\1', book)

# add quotes around what seems like dialog
if add_dialog_quotes:
	book = re.sub(r'\.\W([^\.]*?) ' + pronouns + ' ' + said + '\.', r'.\n\n"\1," \2 \3.\n\n', book)
	book = re.sub(r'\.\W' + pronouns_upper+ ' ' + said + ' ([^\.]*?)\.', r'.\n\n\1 \2, "\3."\n\n', book)

	book = re.sub(r'\.\W([^\.]*?) ' + pronouns + ' ' + asked + '\.', r'.\n\n"\1?" \2 \3.\n\n', book)
	book = re.sub(r'\.\W' + pronouns_upper + ' ' + asked + ' ([^\.]*?)\.', r'.\n\n\1 \2, "\3?"\n\n', book)

	book = re.sub(r'"(\b[a-z])', lambda pat: '"' + pat.group(1).upper(), book)


# end of book! add contributors
book += '\n\nEND\n\n\n\nCONTRIBUTORS\nThis book was made using spam comments by the following authors:\n'
with open(authors_file) as f:
	authors_set = set()
	for author in f:
		authors_set.add(author.strip())
	authors = sorted(authors_set)
	num_authors = len(authors)
	book += '\n'.join(authors)
		


# done! write to file
print '- writing to file...'
with open('output.txt', 'w') as f:
	f.write('SPAM NOVEL' + '\n' + 'Coded by Jeff Thompson and written by ' + str(num_authors) + ' spam authors' + '\n' + '2014')
	f.write('\n\n\nCHAPTER 1\n\n')
	f.write(book)

print '- chapters created: ' + str(chapter)
print 'ALL DONE!'

