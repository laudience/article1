from auth.auth import consumer_key,consumer_secret, access_token, access_token_secret
import tweepy

def get_API():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    return tweepy.API(auth)
