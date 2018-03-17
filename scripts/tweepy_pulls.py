import tweepy, sys, time, re
import datetime, csv
from unidecode import unidecode
import json, os
from random import random

#Load config parameters
params = json.load(open("tweepy_pull_config.json"))

#Define config parameters
consumer_key = params['consumer_key']
consumer_secret = params['consumer_secret']
access_token = params['access_token']
access_token_secret = params['access_token_secret']
out_path = params['out_path']
limit_buffer = params['limit_buffer']
topics = params['topics']
today = datetime.datetime.now()

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Extract the desired information from the specified tweet object
def extract_tweet_columns(tweet):
    user = tweet.user
	
    # Capture any information relevant to the original tweet
	# if this is a retweeted status
    if hasattr(tweet,'retweeted_status'):
        tweet_text = tweet.retweeted_status.full_text
        RT_flag = 'Y'
        rtwt_id = tweet.retweeted_status.id
        rtwt_created_at = tweet.retweeted_status.created_at
        rtwt_user_created_at = tweet.retweeted_status.user.created_at
        rtwt_user = tweet.retweeted_status.user.screen_name
        rtwt_user_id = tweet.retweeted_status.user.id
        rtwt_user_followers = tweet.retweeted_status.user.followers_count
        rtwt_user_friends = tweet.retweeted_status.user.friends_count
        rtwt_user_location = tweet.retweeted_status.user.location
        rtwt_user_time_zone = tweet.retweeted_status.user.time_zone
        rtwt_statuses_count = tweet.retweeted_status.user.statuses_count
    else:
        tweet_text = tweet.full_text
        RT_flag = 'N'
        rtwt_id = ''
        rtwt_created_at = ''
        rtwt_user_created_at = ''
        rtwt_user_id = ''
        rtwt_user = ''
        rtwt_user_followers = ''
        rtwt_user_friends = ''
        rtwt_user_location = ''
        rtwt_user_time_zone = ''
        rtwt_statuses_count = ''
	
    # Capture the count of replies on this tweet
    if hasattr(tweet,'reply_count'):
        reply_count = tweet.reply_count
    else:
        reply_count = 0

    # Capture the count of retweets for this tweet
    if hasattr(tweet,'retweet_count'):
        rtwt_count = tweet.retweet_count
    else:
        rtwt_count = 0
	
    # Capture any hashtags within the tweet
    hashtags = ""
    for hashtag in tweet.entities['hashtags']:
        hashtags = hashtags + " " + hashtag['text']

    # Capture any user mentions within the tweet
    user_mentions = ""
    for mention in tweet.entities['user_mentions']:
        user_mentions = user_mentions + " " + mention['screen_name']

    return [topic,tweet.id,tweet.created_at,reply_count,RT_flag,rtwt_count,hashtags,user_mentions,unidecode(user.screen_name),user.id,unidecode(tweet_text),user.followers_count,user.friends_count,user.favourites_count,user.created_at,user.statuses_count,user.time_zone,user.location,rtwt_id,rtwt_created_at,rtwt_user,rtwt_user_id,rtwt_user_created_at,rtwt_user_followers,rtwt_user_friends,rtwt_user_location,rtwt_user_time_zone,rtwt_statuses_count]


# Begin pulling back twitter data by topic
for topic in topics:
    # Query remaining API search calls to assess if we need to pause
    limit_info = api.rate_limit_status()['resources']['search']['/search/tweets']

    # Read the maximum ID queried from the last twitter data pull
    # to ensure we start pulling data only from after that point
    try:
        f = open("{0}/{1}/{1}_max_id.txt".format(out_path,topic.replace(" ","_").lower()),"r+")
        max_id = int(f.read())
        print("For topic {1}, current max_id is: {0}!".format(max_id,topic))
    except:
        print("First time pulling data for topic {0}!".format(topic))
        max_id = -1
		
    # Ensure the out_file directory for this topic exists.
	# If not, create it.
    if not os.path.exists("{0}/{1}".format(out_path,topic.replace(" ","_").lower())):
        os.makedirs("{0}/{1}".format(out_path,topic.replace(" ","_").lower()))

    # Run search query to pull 100 tweets back based on the defined topic
    tweets = api.search(topic,count=100,since_id=int(max_id),tweet_mode='extended')
    if limit_info['remaining'] > limit_buffer*random() + len(topics):
        print("On topic {1}, have {0} searches left!".format(str(limit_info['remaining']),topic))
        with open("{0}/{1}/{1}_tweets_{2}_{3}_{4}.csv".format(out_path,topic.replace(" ","_").lower(),str(today.month),str(today.day),str(today.year)), 'a+',newline='') as csvfile:
            tweet_writer = csv.writer(csvfile, delimiter=',')
            for tweet in tweets:
                tweet_writer.writerow(extract_tweet_columns(tweet))
                if tweet.id > max_id:
                    max_id = tweet.id

    print("For topic {1} Max ID is : {0}!\n".format(str(max_id),topic))
    f = open("{0}/{1}/{1}_max_id.txt".format(out_path,topic.replace(" ","_").lower()),"w+")
    f.write(str(max_id))
    f.close()
