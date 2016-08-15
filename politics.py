from utilitaires import *
import json


class PoliticsRelations:
    def __init__(self):
        self.api = get_API()
        self.deputies_dict=import_data('data.csv')
        self.relations_dict=init_graph('data.csv')

    def mentions_and_retweets(self, writing=False):
        print("mentions_and_retweets")
        mentions_couple=[]
        retweet_couple=[]
        tweet_count=0
        deputy_count=0
        for deputy in self.deputies_dict:
            deputy_count+=1
            print(deputy_count, self.deputies_dict[deputy], " : ", deputy)
            for tweet in tweepy.Cursor(self.api.user_timeline, id=deputy).items(10):
                if 'retweeted_status' in dir(tweet):
                    if tweet.retweeted_status.user.id_str in self.relations_dict[deputy]:
                        print("add retweet")
                        retweet_couple.append(
                            (deputy, tweet.retweeted_status.user.id_str, tweet.created_at.date(), tweet.id))
                        self.relations_dict[deputy][tweet.retweeted_status.user.id_str]['retweets'] += 1
                    else:
                        for mention in tweet.entities['user_mentions']:
                            if mention['id_str'] in self.relations_dict:
                                print("add mentions")
                                mentions_couple.append((deputy, mention['id_str'], tweet.created_at.date(), tweet.id))
                                self.relations_dict[deputy][mention['id_str']]['mentions'] += 1
                tweet_count+=1
            print(tweet_count)



        print("\n Retweet :",len(retweet_couple), "\n Mentions :", len(mentions_couple),"\n")

        if writing is True:
            with open('relations.json', 'w') as outfile:
                json.dump(self.relations_dict, outfile)
            print("data imported, json writed")


def main():
    PoliticsRelations().mentions_and_retweets(writing=True)



if __name__ == '__main__':
    main()
