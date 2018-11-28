import tweepy
import json
import ngram
import markov
import time
import random
import ConfigParser


def tweetlojifact(api, bot):

    """ A simple helper method to handle the process of sleeping, formatting,
        and sending tweets.

        Params:

        - `api`: a Tweepy API object
        - `bot`: an instance of `markov.MarkovBot`

    """

    while True:
        tmpl = u"loji fact No {0}: {1}"
        factno = random.randint(0, 100000)
        sent = u' '.join(bot.generate_sentence())

        print tmpl.format(factno, sent)
        try:
            api.update_status(status=tmpl.format(factno, sent))
        except:
            pass
        time.sleep(900)


if __name__ == "__main__":
    bot = markov.MarkovBot()
    data = {}
    g1, g2, g3 = ngram.NGram(size=1), ngram.NGram(size=2), ngram.NGram(size=3)
    cf = ConfigParser.ConfigParser()

    # open up our configuration file that has our twitter tokens,
    # and load it into a configuration object we can use to reference
    # our various API keys, without hard coding them into our bot's
    # source code.
    with open('twittertokens.cfg', 'r') as fh:
        cf.readfp(fh)

    # load the JSON corpus of tweets. I've processed this file elsewhere,
    # I'll include some instructions as to what I did there in the readme...
    with open('dump', 'r') as f:
        data = json.load(f)

    # Now that we've loaded the corpus, we need to index it. The process
    # of indexing is basically just loading the 3 "gramstore" objects I
    # created above, and loading each successive tweet into it.
    for tweet in data['tweet']:
        g1.index(tweet)
        g2.index(tweet)
        g3.index(tweet)

    # The bot itself grabs random word-level ngrams from the
    # various stores, you can add or remove as many as you like.
    # Basically, you're just playing with how many words in a row
    # the bot stores in a "chain". see the ngram library for
    # more information there.
    bot.add_gramstore(g1)
    bot.add_gramstore(g2)
    bot.add_gramstore(g3)

    # now that we've setup the above, we need to create the
    # tweepy objects that can actually be used to communicate
    # with twitter.
    auth = tweepy.OAuthHandler(cf.get('keys', 'CONSUMER_KEY'),
                               cf.get('keys', 'CONSUMER_SECRET'))
    auth.set_access_token(cf.get('keys', 'ACCESS_TOKEN'),
                          cf.get('keys', 'ACCESS_SECRET'))
    api = tweepy.API(auth)

    # and away we go. Start posting random non-sense
    tweetlojifact(api, bot)
