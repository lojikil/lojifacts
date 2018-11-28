import json
import re
import random


def stopfilter(word):

    if word[0] == '@' or word.startswith('http'):
        return False

    return True


class NGram(object):
    __slots__ = ['wordindex', 'size', 'punct', 'chain']

    def __init__(self, size=2):
        self.wordindex = {}
        self.chain = {}
        self.size = size
        self.punct = re.compile(r'["\!\^\(\)_\+\*=\{\}\[\]\|:;,<>\.\?]')

    def index(self, words):
        idx = 0
        gram, pgram = '', ''
        words = words.replace('&amp;', '&')
        wlist = filter(stopfilter, re.sub(self.punct, '', words).split())

        if len(wlist) < self.size:
            self.__add_gram__(words)

        wlen = len(wlist) - self.size

        for idx in range(0, wlen):
            tmpgram = []

            for tmp in range(idx, idx + self.size):
                tmpgram.append(wlist[tmp])

            gram = ' '.join(tmpgram)

            self.__add_gram__(gram)

            if pgram is not '':
                self.__add_chain__(pgram, gram)

            pgram = gram

    def random_gram(self):
        """ return a random ngram from the corpus """
        return random.choice(self.wordindex.keys())

    def gram_starts_with(self, prefix):
        """ given a prefix, return a (gram, chain) tuple that
            starts with prefix."""

        if prefix in self.chain:
            return (prefix, self.chain[prefix])

        for k, v in self.chain.iteritems():
            # print "here: {0}".format(k)
            if k.startswith(prefix):
                return (k, v)

        return None

    def __add_gram__(self, gram):

        if gram in self.wordindex:
            self.wordindex[gram] += 1
        else:
            self.wordindex[gram] = 1

    def __add_chain__(self, pgram, gram):

        if pgram in self.chain:
            self.chain[pgram].add(gram)
        else:
            self.chain[pgram] = set([gram])

    def gram_stats(self):
        wdata = []
        for i in self.wordindex.iteritems():
            wdata.append(i)
            if len(wdata) > 10:
                wdata = sorted(wdata, key=lambda x: x[1], reverse=True)
                wdata = wdata[0:10]

        return wdata


if __name__ == "__main__":

    data, gramindex = {}, NGram()
    gramind3x = NGram(size=3)
    gram1ndex = NGram(size=1)

    with open('dump', 'r') as f:
        data = json.load(f)

    for tweet in data['tweet']:
        gramindex.index(tweet)
        gramind3x.index(tweet)
        gram1ndex.index(tweet)

    print gramindex.wordindex.keys()[0:10]
    print gramind3x.wordindex.keys()[0:10]
    print gram1ndex.wordindex.keys()[0:10]
    print gramindex.gram_stats()
    print gramind3x.gram_stats()
    print gram1ndex.gram_stats()
    print gramindex.chain.items()[0:10]
    print gramind3x.chain.items()[0:10]
    print gram1ndex.chain.items()[0:10]
    print gramindex.random_gram()
    print gramind3x.random_gram()
    print gram1ndex.random_gram()
