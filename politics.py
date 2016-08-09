from utilitaires import *
import csv
import json


class PoliticsRelations:
    def __init__(self):
        self.api = get_API()
        self.deputies_dict=dict()
        self.relations_dict=dict()

    def import_data_from_csv(self):
        with open('data.csv', 'r', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.deputies_dict[row[1]]=dict() # importe les relations id_str -> screen_name pour eviter d'avoir à relire le csv à chaque fois
                self.deputies_dict[row[1]]=row[0]
                self.relations_dict[row[1]]=dict()
                for row2 in reader:
                    self.relations_dict[row[1]][row2[1]]=dict() # On utilise les idr_str comme index
                    self.relations_dict[row[1]][row2[1]]['retweets']=0
                    self.relations_dict[row[1]][row2[1]]['mentions']=0 # relations_dict[depute1][depute2]=nombre de retweet du depute2 fait par le depute1
        print("Deputies datas in dictionnary")

    def mentions_and_retweets(self, writing=False):
        self.import_data_from_csv()
        mentions_couple=[]
        retweet_couple=[]
        deputy_count=0
        tweet_count=0
        for deputy in self.relations_dict:
            while tweet_count < 30: # Pour le dev
                for tweet in tweepy.Cursor(self.api.user_timeline, id=self.relations_dict[deputy]).items(2):
                    if 'retweeted_status' in dir(tweet):
                        retweet_couple.append((deputy, tweet.retweeted_status.user.id_str, tweet.created_at.date(),tweet.id))
                        if tweet.retweeted_status.user.id_str in self.relations_dict:
                            self.relations_dict[deputy][tweet.retweeted_status.user.id_str]['retweet']+=1
                    else:
                        for mention in tweet.entities['user_mentions']:
                            mentions_couple.append((deputy,mention['id_str'], tweet.created_at.date(),tweet.id))
                            if tweet.retweeted_status.user.id_str in self.relations_dict:
                                self.relations_dict[deputy][tweet.retweeted_status.user.id_str]['mentions'] += 1
                    tweet_count+=1
                    print(tweet_count)
            deputy_count+=1
            print(deputy_count)

        print("\n Retweet :",retweet_couple, "\n Mentions :", mentions_couple,"\n")

        if writing is True:
            with open('relations.json', 'w') as outfile:
                json.dump(self.relations_dict, outfile)
            print("data imported, json writed")


def main():
    PoliticsRelations().mentions_and_retweets(writing=True)



if __name__ == '__main__':
    main()