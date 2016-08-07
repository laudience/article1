from connection import *

api = get_API()

deputies_list=[]
assemblee_nationale = api.get_user('AssembleeNat')
for user in tweepy.Cursor(api.list_members, assemblee_nationale.screen_name, 'les-deputes').items():
    deputies_list.append(user.name)

mentions_couple=[]
retweet_couple=[]
i=0
for deputy in deputies_list[3:4]:
    for tweet in tweepy.Cursor(api.user_timeline, id=deputy).items(200):
        if 'retweeted_status' in dir(tweet):
            retweet_couple.append((deputy, tweet.retweeted_status.user.name, tweet.created_at.date(),tweet.id))
        else:
            for mention in tweet.entities['user_mentions']:
                mentions_couple.append((deputy,mention['screen_name'], tweet.created_at.date(),tweet.id))
        i+=1
print("\n Retweet :",retweet_couple, "\n Mentions :", mentions_couple,"\n",i)




