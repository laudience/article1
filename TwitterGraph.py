from utilitaires import *
import json

class TwitterGraph:
    def __init__(self, api):
        self.api = api
        self.nodes = {}
        self.links = {}

        self.nbItems = 10

    #___processTweet____________________________________________
    
    def process_tweet(self, tweet, source):
        if 'retweeted_status' in dir(tweet):
            target = tweet.retweeted_status.user.id_str
            if target in self.links[source]:
                self.add_retweet(source, target)

        for mention in tweet.entities['user_mentions']:
            target = mention['id_str']
            if target in self.links[source]:
                self.add_mention(source, target)
                
    #___addRetweet______________________________________________
    
    def add_retweet(self, source, target):
        self.links[source][target]['retweets'] += 1

    #___addMention______________________________________________
    
    def add_mention(self, source, target):
        self.links[source][target]['mention'] +=1

    #___init_from_csv___________________________________________

    def init_from_csv(self, filename):
        self.init_nodes(filename)
        self.init_links(filename)
        
    #___initNodes_______________________________________________
    
    def init_nodes(self, filename):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                self.nodes[row['id']] = row['user_name']

    #___initLinks_______________________________________________

    def init_links(self, filename):
        with open(filename, 'r') as fst_file:
            fst_reader = csv.DictReader(fst_file, delimiter=";")
        
            for source in fst_reader:
                with open(filename, 'r') as snd_file:
                    snd_reader = csv.DictReader(snd_file, delimiter=";")
                    self.links[source['id']] = dict()
                    
                    for target in snd_reader:
                        self.links[source['id']][target['id']] = { "retweets": 0, "mentions": 0 }

    
    #___readJSON________________________________________________
    
    def read_json(self, csv_filename, json_filename): #seb
        self.init_nodes(csv_filename)
        with open(json_filename, 'r') as infile:
            self.links = json.load(infile)

    #___constructGraph__________________________________________
    
    def construct_graph(self):
        for node in self.nodes:
            for tweet in tweepy.Cursor(self.api.user_timeline, id=node).item(self.nbItems):
                self.process_tweet(tweet, node)

    #___saveTwitterGraph________________________________________
                
    def save_twitter_graph(self, outfile_name): #seb
        with open(outfile_name, 'w') as outfile:
            json.dump(self.links, outfile)

    #___plotGraph_______________________________________________
    
#    def plot_graph(self): # -----
    
    
def main():
    test  = TwitterGraph(get_API())

    filename = "test.csv"
    test.init_from_csv(filename)
    test.save_twitter_graph("test.json")


if __name__ == '__main__':
    main()
