from auth.auth import consumer_key,consumer_secret, access_token, access_token_secret
import tweepy
import csv

#___get_API________________________________________________________

def get_API():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    

    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify = True)

#____save_list_____________________________________________________

def save_list(api, usr_str, list_name, filename):
    with open(filename, 'w') as csvfile:
        fieldnames = ['user_name', 'id']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames, delimiter=";")

        writer.writeheader()

        usr = api.get_user(usr_str)
        for member in tweepy.Cursor(api.list_members, usr.screen_name, list_name).items():
            if member.protected is False:
                writer.writerow({'user_name' : member.name , 'id' : member.id_str})
    print("data imported, csv writed")

#___import_data____________________________________________________

def import_data(filename):
    data=dict()
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            data[row['id']] = row['user_name']
    return data

#___init_graph_____________________________________________________

def init_graph(filename):
    graph=dict()
    
    with open(filename, 'r') as fst_file:
        fst_reader = csv.DictReader(fst_file, delimiter=";")
        
        for row_fst_r in fst_reader:
            
            with open(filename, 'r') as snd_file:
                snd_reader = csv.DictReader(snd_file, delimiter=";")
                graph[row_fst_r['id']] = dict()
                
                for row_snd_r in snd_reader:
                    graph[row_fst_r['id']][row_snd_r['id']] = { "retweets": 0, "mentions": 0 }
    return graph
