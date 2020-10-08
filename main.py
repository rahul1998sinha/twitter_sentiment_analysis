import re  # REGULAR EXPRESSION
import tweepy  # TWITTER API FOR PYTHON
from tweepy import OAuthHandler
from textblob import TextBlob  # FOR NLP
import matplotlib.pyplot as plt


class connection_twitter_api(object):
    def __init__(self):
        print('Establishing Connection.....')

    def establish_connection(self):
        consumer_key = 'xxxxxxxxxxxxxxxxx' #enter the consumer key from twitter api
        consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxx' #enter the consumer secret key from twitter api
        access_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #enter the acess key from twitter api
        access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #enter the acess token key from twitter api
        try:
            self.authenticated = OAuthHandler(consumer_key, consumer_secret)
            self.authenticated.set_access_token(access_key, access_token)
            self.api = tweepy.API(self.authenticated)
        except:
            print("Error: Authentication Failed")

    def tweet_trimer(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())

    def analyize_tweet(self, tweet):
        analysis = TextBlob(self.tweet_trimer(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def display_tweets(self, tweets):
        print("---Rendering Tweets LIVE-----")
        for tweet in tweets:
            print(tweet['text'])

    def get_tweets(self, query, count=10):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                if tweet.lang == "en":
                    parsed_tweet = {'text': tweet.text, 'sentiment': self.analyize_tweet(tweet.text)}
                    if tweet.retweet_count > 0:
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)

            return tweets
        except tweepy.TweepError as e:
            print("Error : " + str(e))


if __name__ == '__main__':
    api = connection_twitter_api()
    connection_twitter_api.establish_connection(api)
    tweets = api.get_tweets(query='India', count=100)
    connection_twitter_api.display_tweets(api, tweets)
    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("\n\nPositive tweets:")
    for tweet in positive_tweets[:10]:
        print(tweet['text'])
    print("\n\nNegative tweets:")
    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    for tweet in negative_tweets[:10]:
        print(tweet['text'])
    source = ['positive', 'negative', 'neutral']
    data = list()
    data.append(len(positive_tweets))
    data.append(len(negative_tweets))
    data.append(len(tweets) - len(positive_tweets) - len(negative_tweets))
    print("Positive tweets percentage: {} %".format(100 * len(positive_tweets) / len(tweets)))
    print("Negative tweets percentage: {} %".format(100 * len(negative_tweets) / len(tweets)))
    print("Neutral tweets percentage: {} % \
              ".format(100 * (len(tweets) - (len(negative_tweets) + len(positive_tweets))) / len(tweets)))
    fig = plt.figure(figsize=(5, 5))
    plt.pie(data, labels=source)
    plt.legend()
    plt.show()
