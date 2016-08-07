from auth.auth import consumer_key,consumer_secret, access_token, access_token_secret
import tweepy


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

deputies_list=[]
assemblee_nationale = api.get_user('AssembleeNat')
for user in tweepy.Cursor(api.list_members, assemblee_nationale.screen_name, 'les-deputes').items():
    deputies_list.append(user.name)

links=[]
for deputy in deputies_list[:5]:
    for tweet in api.user_timeline(id=deputy,count=5):
        for mention in tweet.entities['user_mentions']:
            links.append((deputy,mention['screen_name']))
print(links)




