from auth.auth import consumer_key,consumer_secret, access_token, access_token_secret
import tweepy
import csv

def get_API():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    return tweepy.API(auth)

def save_list(api, usr_str, list_name, filename):
    with open(filename, 'w') as csvfile:
        fieldnames = ['user_name', 'id']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames, delimiter=";")

        writer.writeheader()

        usr = api.get_user(usr_str)
        for member in tweepy.Cursor(api.list_members, usr.screen_name, list_name).items():
            writer.writerow({'user_name' : member.name , 'id' : member.id_str})
    print("data imported, csv writed")

def import_data_from_csv(filename):
    data={}
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            data[row['id']] = row['user_name']
    return data
