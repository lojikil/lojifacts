import json
import re


punct = re.compile(r'[\'"\\/\*\!@#$%\^&\(\)_\-\+=\{\}\[\]\|:;,<>\.\?]')


def stopfilter(x):

    if x[0] == '@' or x.startswith('http') or x[0] == '#' or x[0] == '&':
        return False

    x = re.sub(punct, '', x)

    if x == '':
        return False

    return not x.lower() in stopwords

data = None
stopwords = []
word_index = {}

with open('dump', 'r') as f:
    data = json.load(f)

with open('stopwords.dat', 'r') as f:
    stopwords = [x.strip() for x in f.readlines()]

for tweet in data['tweet']:
    words = [x.lower() for x in filter(stopfilter, tweet.split())]
    for word in words:
        word = re.sub(punct, '', word.lower())
        if word in word_index:
            word_index[word] += 1
        else:
            word_index[word] = 1

print len(word_index.keys())

data = []
for i in word_index.iteritems():
    data.append(i)
    if len(data) > 100:
        data = sorted(data, key=lambda x: x[1], reverse=True)
        data = data[0:100]

print data
