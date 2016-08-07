from utilitaires import *
import csv


class PoliticsRelations:
    def __init__(self):
        self.api = get_API()
        self.deputies_dict=dict()

    def import_data_from_csv(self):
        with open('data.csv', 'r', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.deputies_dict[row[0]]=dict()
                self.deputies_dict[row[0]]['id_str']=row[1]
        print("Deputies datas in dictionnary")

    def mentions_and_retweets(self):
        self.import_data_from_csv()
        mentions_couple=[]
        retweet_couple=[]
        deputy_count=0
        tweet_count=0
        for deputy in self.deputies_dict:
            for tweet in tweepy.Cursor(self.api.user_timeline, id=self.deputies_dict[deputy]['id_str']).items(1):
                if 'retweeted_status' in dir(tweet):
                    retweet_couple.append((deputy, tweet.retweeted_status.user.name, tweet.created_at.date(),tweet.id))
                else:
                    for mention in tweet.entities['user_mentions']:
                        mentions_couple.append((deputy,mention['screen_name'], tweet.created_at.date(),tweet.id))
                tweet_count+=1
                print(tweet_count)
            deputy_count+=1
            print(deputy_count)

        print("\n Retweet :",retweet_couple, "\n Mentions :", mentions_couple,"\n")


def main():
    PoliticsRelations().mentions_and_retweets()



if __name__ == '__main__':
    main()