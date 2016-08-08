from utilitaires import *
import csv


class PoliticsRelations:
    def __init__(self):
        self.api = get_API()
        self.deputies_dict=dict()
        self.retweets_dict=dict()

    def import_data_from_csv(self):
        with open('data.csv', 'r', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.deputies_dict[row[1]]=dict() # importe les relations id_str -> screen_name pour eviter d'avoir à relire le csv à chaque fois
                self.deputies_dict[row[1]]=row[0]
                self.retweets_dict[row[1]]=dict()
                for row2 in reader:
                    self.retweets_dict[row[1]][row2[1]]=0# relations_dict[depute1][depute2]=nombre de retweet du depute2 fait par le depute1
        print("Deputies datas in dictionnary")

    def mentions_and_retweets(self, writing=False):
        self.import_data_from_csv()
        mentions_couple=[]
        retweet_couple=[]
        deputy_count=0
        tweet_count=0
        for deputy in self.retweets_dict:
            for tweet in tweepy.Cursor(self.api.user_timeline, id=self.retweets_dict[deputy]).items(2):
                if 'retweeted_status' in dir(tweet):
                    retweet_couple.append((deputy, tweet.retweeted_status.user.id_str, tweet.created_at.date(),tweet.id))
                    if tweet.retweeted_status.user.id_str in self.retweets_dict:
                        self.retweets_dict[deputy][tweet.retweeted_status.user.id_str]+=1
                else:
                    for mention in tweet.entities['user_mentions']:
                        mentions_couple.append((deputy,mention['screen_name'], tweet.created_at.date(),tweet.id))
                tweet_count+=1
                print(tweet_count)
            deputy_count+=1
            print(deputy_count)

        print("\n Retweet :",retweet_couple, "\n Mentions :", mentions_couple,"\n")

        if writing is True:
            with open('relations', 'w') as csvfile:
                fieldnames = [id_str for id_str in self.deputies_dict]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

                writer.writeheader()

                for deputy in self.retweets_dict:
                    writer.writerow(self.retweets_dict[deputy])
            print("data imported, csv writed")


def main():
    PoliticsRelations().mentions_and_retweets()



if __name__ == '__main__':
    main()