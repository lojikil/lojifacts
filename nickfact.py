import ngram
import markov
import time
import random


def nickfact(bot):

    """ A simple helper method to handle the process of sleeping, formatting,
        and sending tweets.

        Params:

        - `api`: a Tweepy API object
        - `bot`: an instance of `markov.MarkovBot`

    """

    while True:
        tmpl = u"NickDe fact No {0}: {1}"
        factno = random.randint(0, 100000)
        try:
            sent = u' '.join(bot.generate_sentence())

            print tmpl.format(factno, sent)
            time.sleep(3600)
        except:
            pass


if __name__ == "__main__":
    bot = markov.MarkovBot()
    data = {}
    g1, g2, g3 = ngram.NGram(size=1), ngram.NGram(size=2), ngram.NGram(size=3)

    with open('nick-facts.txt', 'r') as f:
        for line in f:
            line = line.strip()
            g1.index(line)
            g2.index(line)
            g3.index(line)

    # The bot itself grabs random word-level ngrams from the
    # various stores, you can add or remove as many as you like.
    # Basically, you're just playing with how many words in a row
    # the bot stores in a "chain". see the ngram library for
    # more information there.
    bot.add_gramstore(g1)
    bot.add_gramstore(g2)
    bot.add_gramstore(g3)

    # and away we go. Start posting random non-sense
    nickfact(bot)
