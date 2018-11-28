import ngram
import random
import json


class MarkovBot(object):

    def __init__(self, gramstores=None):
        if gramstores is None:
            self.gramstores = []
        else:
            self.gramstores = gramstores

    def add_gramstore(self, gramstore):
        self.gramstores.append(gramstore)

    def _stitch(self, terms):
        total = ' '.join(terms).split()
        prev = ''
        res = []
        for idx in total:
            if idx != prev:
                res.append(idx)
                prev = idx
        return res

    def generate_sentence(self):

        rs = []

        store = random.choice(self.gramstores)
        gram = store.random_gram()
        for rnd in range(0, 5):
            rs.append(gram)
            potential = store.gram_starts_with(gram)

            if potential is None:
                continue

            chgram = random.choice(list(potential[1]))

            if chgram is set:
                chgram = list(chgram)[0]

            rs.append(chgram)

            if ' ' in chgram:
                gram = chgram.split()[-1]  # take the last gram for searching
            else:
                gram = chgram

            store = random.choice(self.gramstores)

        return self._stitch(rs)


if __name__ == "__main__":
    bot = MarkovBot()
    data = {}
    g1, g2, g3 = ngram.NGram(size=1), ngram.NGram(size=2), ngram.NGram(size=3)

    with open('dump', 'r') as f:
        data = json.load(f)

    for tweet in data['tweet']:
        g1.index(tweet)
        g2.index(tweet)
        g3.index(tweet)

    bot.add_gramstore(g1)
    bot.add_gramstore(g2)
    bot.add_gramstore(g3)

    print bot.generate_sentence()
