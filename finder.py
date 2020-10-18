import load_files as lf 

FUZZINESS = 0.5 # Toggle percent of words that must match to be returned 
POTENTIALS = 10 # How many non-exact matches to show if search fails

meta = lf.load_db()
print("Press q to cancel")
search_text = None

while search_text != 'q':
	findwhat = input("\n\nWHAT LINE ARE U LOOKING FOR: ")
	search_text = lf.clean_text(findwhat)
	keywords = search_text.split(' ')

	# First check potential matches; matches that share at least 
	# FUZZINESS% of the words with the search (a lot less expensive 
	# than rote comparison for an exact phrase)
	potential_matches = []
	for t,m in meta.items():
		hits = len(set(keywords).intersection(m['unique']))
		if hits > int(len(set(keywords)) * FUZZINESS):
			potential_matches.append((hits,t))

	# Takes O(n logn) time but increases liklihood of early exact match
	# found. Also saves time on organizing guesses if exact not found
	potential_matches.sort() 

	# Now check for an exact match out of the potentials
	exact_found = False
	for _,t in potential_matches:
		m = meta[t]

		if search_text in m['script']:
			print('"%s" is said in %s\nhttps://youtube.com/%s' % (search_text, m['title'], t))
			exact_found = True

	if not exact_found:
		if len(potential_matches) == 0:
			print("Sorry, couldn't find a video where he said anything like that")
			continue 

		potential_matches = potential_matches[:POTENTIALS]
		print("I didn't find an exact match, but these are pretty close:")
	
		for i in range(len(potential_matches)):
			m = meta[potential_matches[i][1]]
			t = potential_matches[i][1]
			print("[%d]\t%s,  https://youtube.com/%s" % (i, m['title'], t))