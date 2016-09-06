from utilitaires import *
import json

class TwitterGraph:
    def __init__(self, api):
        self.api = api
        self.nodes = {}
        self.links = {}

        self.nbItems = 10

    #___processTweet____________________________________________
    
    def processTweet(tweet, source):
        if 'retweeted_status' in dir(tweet):
            target = tweet.retweeted_status.user.id_str
            if target in self.links[source]:
                addRetweet(source, target)

        for mention in tweet.entities['user_mentions']:
            target = mention['id_str']
            if target in self.links[source]:
                addMention(source, target)
                
    #___addRetweet______________________________________________
    
    def addRetweet(source, target):
        self.links[source][target]['retweets'] += 1

    #___addMention______________________________________________
    
    def addMention(source, target): 
        self.links[source][target]['mention'] +=1

    #___init_from_csv___________________________________________

    def init_from_csv(self, filename):
        initNodes(filename)
        init_links(filename)
        
    #___initNodes_______________________________________________
    
    def initNodes(filename): 
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
    
    def readJSON(filename): #seb

    #___constructGraph__________________________________________
    
    def constructGraph(): 
        for node in self.nodes:
            for tweet in tweepy.Cursor(self.api.user_timeline, id=node).item(self.nbItems):
                processTweet()

    #___saveTwitterGraph________________________________________
                
    def saveTwitterGraph(str_name): #seb

    #___plotGraph_______________________________________________
    
    def plotGraph(): # -----
    
    
def main():
    test  = TwitterGraph()

    filename = "test.csv"
    test.init_from_csv(filename)



if __name__ == '__main__':
    main()
