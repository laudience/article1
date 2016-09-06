import igraph as ig
import plotly
import plotly.graph_objs as go
from utilitaires import *
import json

class TwitterGraph:
    def __init__(self, api):
        self.api = api
        self.nodes = {}
        self.links = {}

        self.nbItems = 100

    #___processTweet____________________________________________
    
    def process_tweet(self, tweet, source):
        if 'retweeted_status' in dir(tweet):
            target = tweet.retweeted_status.user.id_str
            if target in self.links[source]:
                print("retweet : ( source :", source, "target : ", target, ") : ", tweet.created_at)
                self.add_retweet(source, target)

        for mention in tweet.entities['user_mentions']:
            target = mention['id_str']
            if target in self.links[source]:
                print(tweet.created_at)
                self.add_mention(source, target)
                
    #___addRetweet______________________________________________
    
    def add_retweet(self, source, target):
        self.links[source][target]['retweets'] += 1

    #___addMention______________________________________________
    
    def add_mention(self, source, target):
        self.links[source][target]['mentions'] +=1

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
            for tweet in tweepy.Cursor(self.api.user_timeline, id=node).items(self.nbItems):
                self.process_tweet(tweet, node)

    #___saveTwitterGraph________________________________________
                
    def save_twitter_graph(self, outfile_name): #seb
        with open(outfile_name, 'w') as outfile:
            json.dump(self.links, outfile)

    #___plotGraph_______________________________________________
    
    def plot_graph(self, link_type):
        Nodes = [deputy for deputy in self.nodes]
        Edges = []
        for deputy1 in Nodes:
            for deputy2 in self.links[deputy1]:
                if self.links[deputy1][deputy2][link_type] != 0:
                    Edges.append((Nodes.index(deputy1), Nodes.index(deputy2)))
        G=ig.Graph(Edges, directed=True)
        N=len(Nodes)
        print(N)
        labels = [self.nodes[Nodes[i]] for i in range(N)]
        layt = G.layout('auto',dim=2)
        Xn = [layt[k][0] for k in range(N)]
        Yn = [layt[k][1] for k in range(N)]
                    
        Xe = []
        Ye = []
                    
        for e in Edges:
            print(e)
            Xe += [layt[e[0]][0], layt[e[1]][0], None]
            Ye += [layt[e[0]][1], layt[e[1]][1], None]
                        
                        
            trace1 = go.Scatter(x=Xe,
                                            y=Ye,
                                            mode='lines',
                                            line=go.Line(color='rgb(125,125,125)', width=1),
                                            hoverinfo='none'
                        )
            trace2 = go.Scatter(x=Xn,
                                            y=Yn,
                                            mode='markers',
                                            name='deputies',
                                            marker=go.Marker(symbol='dot',
                                                             size=6,
                                                             colorscale='Viridis',
                                                             line=go.Line(color='rgb(50,50,50)', width=0.5)
                                            ),
                                            text=labels,
                                            hoverinfo='text'
                        )
            axis = dict(showbackground=False,
                                    showline=False,
                                    zeroline=False,
                                    showgrid=False,
                                    showticklabels=False,
                                    title='')
            layout = go.Layout(title="Test",
                                           width=1000,
                                           height=1000,
                                           showlegend=False,
                                           hovermode='closest')
            data = go.Data([trace1, trace2])
            fig = go.Figure(data=data, layout=layout)
                        
            plotly.offline.plot(fig, filename=''.join([link_type,'-','relation.html']))
                        
                        
                        
def main():
    test = TwitterGraph(get_API())

    csv_file = "test.csv"
    test.init_from_csv(csv_file)
    test.construct_graph()
    test.save_twitter_graph("test.json")

    json_file = "test.json"

    test2 = TwitterGraph(get_API())
    test2.read_json(csv_file, json_file)
    test2.save_twitter_graph("test2.json")
    test2.plot_graph(link_type='retweets')

if __name__ == '__main__':
    main()
