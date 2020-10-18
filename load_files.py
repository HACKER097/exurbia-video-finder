import os
import re 
import pickle
import string 
import nltk 

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

LEMMATIZER = WordNetLemmatizer()
STOPWORDS = set(stopwords.words('english'))

NUMBERS = '0123456789'
no_punc = re.compile('[%s]' % re.escape(string.punctuation))

def clean_text(s):
    s = s.lower()
    s = no_punc.sub('', s)
    t = nltk.word_tokenize(s)
    t = [LEMMATIZER.lemmatize(w) for w in t]
    t = [w for w in t if w not in STOPWORDS]
    s = ' '.join(t)

    return s


'''
Iterates through everything in /data and builds a data structure 
with just those files
'''
def create_new(data_dir='data', outf='metadata.dat', video_info={}):
    for fname in os.listdir(data_dir):
        # Assumes files are formatted NAME-yt url
        title, url = fname.split('-')[0:2]
        fname = os.path.join(data_dir, fname)

        # Trim file extention from file name
        url = url.split('.')[0]
        
        script = ''
        timecodes = []

        with open(fname, 'r', encoding='utf-8') as f:
            # First 3 lines are metadata and line 4 is blank; last line blank
            text = f.read()
            lines = text.split('\n')[4:-1]
            
            tc_ptr = 0
            
            # Files are formatted irregularly. Hopefully this fixes it. First line is always time code
            # Then continues until blank line signifying next time code
            i = 0
            while i < len(lines):
                tc = lines[i]
                
                # Iterate through all lines of dialogue
                i += 1
                new_lines = ''
                while lines[i] != '':
                    new_lines += clean_text(lines[i]) + ' '
                    i += 1
                
                new_chars = len(new_lines)
                script += new_lines

                # Save timecodes in CSR-like format (start_word_idx, formatted_tc)
                tc = tc.split(':')
                tc = int(tc[1])*60 + int(tc[2].split('.')[0])
                timecodes.append((tc_ptr, tc))
                tc_ptr += new_chars

                # Skip last whitespace line delimeter
                i += 1

            
        script = script[:-1] # Trim tailing space
        unique = set(script.split(' ')) # For faster searching 

        video_info[url] = {'title': title, 'script': script, 'unique': unique, 'timecodes': timecodes}
    
    # Saved compressed dict of metadata
    pickle.dump(video_info, open(outf, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
    return video_info


'''
Adds new video metadata to existing metadata file
Assumes data_dir contains new files and outf already exists
'''
def add_to_db(data_dir='data', outf='metadata.dat'):
    video_info = pickle.load(open(outf, 'rb'))
    return create_new(data_dir=data_dir, outf=outf, video_info=video_info)
    
def load_db(fname='metadata.dat'):
    return pickle.load(open(fname, 'rb'))

if __name__ == '__main__':
    create_new()