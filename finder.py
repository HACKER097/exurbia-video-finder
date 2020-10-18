import load_files as lf 

FUZZINESS = 0.25 # Toggle percent of words that must match to be returned 
POTENTIALS = 10 # How many non-exact matches to show if search fails

meta = lf.load_db()

def prompt():
	findwhat = input("\n\nWHAT LINE ARE U LOOKING FOR: ")
	return lf.clean_text(findwhat)

def display(search_result, meta):
	if len(search_result['exact']):
		for t in search_result['exact']:
			m = meta[t.split('&')[0]]
			print('"%s" is said in %s\nhttps://youtube.com/%s' % (search_text, m['title'], t))

		return 

	if len(search_result['potential']):
		print("I didn't find an exact match, but these are pretty close:")

		p = search_result['potential']
		for i in range(len(p)):
			m = meta[p[i][1]]
			t = p[i][1]
			print("[%d]\t%s,  https://youtube.com/%s" % (i, m['title'], t))

		return 

	print("Sorry, couldn't find a video where he said anything like that")


def search(search_text):
	keywords = search_text.split(' ')
	ret = {'exact': [], 'potential': []} 

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
	for _,u in potential_matches:
		m = meta[u]

		idx = m['script'].find(search_text)
		if idx >= 0:
			# Find matching timecode
			for tc_dat in m['timecodes']:
				if tc_dat[0] > idx:
					break 

				tc = tc_dat[1]

			ret['exact'].append('%s&t=%ss' % (u,tc))
			exact_found = True

	if not exact_found:
		potential_matches = potential_matches[:POTENTIALS]
		ret['potential'] = potential_matches
	
	return ret 

if __name__ == '__main__':
	print("Press q to cancel")

	search_text = prompt()
	while search_text != 'q':
		r = search(search_text)
		display(r, meta)
		search_text = prompt()
	