from utilitaires import *
import csv
import json


class PoliticsRelations:
    def __init__(self):
        self.api = get_API()
        self.deputies_dict=import_data('data.csv')
        self.relations_dict=init_graph('data.csv')

    def mentions_and_retweets(self, writing=False):
        print("mentions_and_retweets");
        mentions_couple=[]
        retweet_couple=[]
        tweet_count=0
        #print(self.api.list_timeline('AssembleeNat', 'les-deputes'))
        for page in tweepy.Cursor(self.api.list_timeline, 'AssembleeNat', 'les-deputes',since_id=676170131362308097).pages(20):
            for tweet in page:

                #print(tweet.author.id_str)
                if 'retweeted_status' in dir(tweet):
                    retweet_couple.append((tweet.author.id_str, tweet.retweeted_status.user.id_str, tweet.created_at,tweet.id))
                    if tweet.retweeted_status.user.id_str in self.relations_dict[tweet.author.id_str]:
                        print("add retweet",self.deputies_dict[tweet.author.id_str],self.deputies_dict[tweet.retweeted_status.user.id_str],tweet.created_at.date(),tweet.id)
                        self.relations_dict[tweet.author.id_str][tweet.retweeted_status.user.id_str]['retweets']+=1
                    else:
                        for mention in tweet.entities['user_mentions']:
                            mentions_couple.append((tweet.author.id_str,mention['id_str'], tweet.created_at.date(),tweet.id))
                            if tweet.retweeted_status.user.id_str in self.relations_dict[tweet.author.id_str]:
                                print("add mentions",self.deputies_dict[tweet.author.id_str],self.deputies_dict[tweet.retweeted_status.user.id_str],tweet.created_at,tweet.id)
                                self.relations_dict[tweet.author.id_str][tweet.retweeted_status.user.id_str]['mentions'] += 1
                tweet_count+=1
            #print(tweet_count)

        print("\n Retweet :",len(retweet_couple), "\n Mentions :", len(mentions_couple),"\n")

        if writing is True:
            with open('relations.json', 'w') as outfile:
                json.dump(self.relations_dict, outfile)
            print("data imported, json writed")


def main():
    PoliticsRelations().mentions_and_retweets(writing=True)



if __name__ == '__main__':
    main()
