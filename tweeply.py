from dotenv import load_dotenv
from time import sleep
import tweepy
import os

load_dotenv()

CONSUMER_KEY=os.getenv('CONSUMER_KEY')
CONSUMER_SECRET=os.getenv('CONSUMER_SECRET')
ACCESS_KEY=os.getenv('ACCESS_KEY')
ACCESS_SECRET=os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

file_name = 'last_seen.txt'

def retrieve_lastseen_id(file_name):
    f_read = open(file_name, 'r')
    lastseen_id = int(f_read.read().strip())
    f_read.close()
    return lastseen_id

def store_lastseen_id(lastseen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(lastseen_id))
    f_write.close()
    return

last_seen_id = retrieve_lastseen_id(file_name)

mention_keyword = 'hai:)'

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_lastseen_id(file_name)
    mentions = api.mentions_timeline(
        last_seen_id,
        tweet_mode='extended'
    )

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_lastseen_id(last_seen_id, file_name)
        if mention_keyword in mention.full_text.lower():
            print('found hai:)', flush=True)
            print('replying...', flush=True)
            api.update_status('@' + mention.user.screen_name + ' hai juga:) syg', mention.id)

while True:
    reply_to_tweets()
    sleep(15)