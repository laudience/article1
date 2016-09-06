from utilitaires import *
import json

class TwitterGraph:
    def __init__(self, api):
        self.api = api
        self.nodes = {}
        self.links = {}

        self.nbItems = 10

    #___processTweet____________________________________________
    
    def processTweet(tweet): #seb

    #___addRetweet______________________________________________
        
    def addRetweet(source, target):
        self.links[source][target]['retweets'] += 1

    #___addMention______________________________________________
    
    def addMention(source, target): 
        self.links[source][target]['mention'] +=1

    #___initNode________________________________________________
    
    def initNode(filename): 
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                self.nodes[row['id']] = row['user_name']
                
    #___readJSON________________________________________________
    
    def readJSON(filename): #seb

    #___constructGraph__________________________________________
    
    def constructGraph(): #gui
        for node in self.nodes:
            for tweet in tweepy.Cursor(self.api.user_timeline, id=node).item(self.nbItems):
                processTweet()

    #___saveTwitterGraph________________________________________
                
    def saveTwitterGraph(str_name): #seb

    #___plotGraph_______________________________________________
    
    def plotGraph(): # -----
    
    
