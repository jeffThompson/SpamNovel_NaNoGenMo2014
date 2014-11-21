
'''
PARSE COMMENTS, EXTRACT SPAM
Jeff Thompson | 2014 | www.jeffreythompson.org

57,994 comments from both my blogs!

'''

import csv, re

comments_file = 	'BlogComments.csv'
comments_output = 	'Comments.txt'
authors_output = 	'Authors.txt'
remove_html = 		True
num_spam_comments =	0


comments = ''
authors = [ ]
with open(comments_file) as f:
	data = csv.reader(f, quotechar='"')
	for index, listing in enumerate(data):
		
		# spam only, please!
		if listing[10] == 'spam':
			
			# who wrote it?
			author = listing[2]
			if len(author) > 0:
				authors.append(author)

			# what did they say?
			comment = listing[8]
			if remove_html:
				comment = re.sub('<[^<]+?>', '', comment)
				comment = re.sub('\[url.*?\]', '', comment)
				comment = re.sub('\[/url]', '', comment)
			comments += comment + ' '
			num_spam_comments += 1


with open(comments_output, 'w') as f:
	f.write(comments)

with open(authors_output, 'w') as f:
	authors = sorted(authors)
	f.write(('\n').join(authors))


print 'Added', num_spam_comments, 'spam comments!'
print 'Written by', len(authors), 'authors!'

