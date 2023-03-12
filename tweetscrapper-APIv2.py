#!/usr/bin/python3
import sys
import tweepy
import time
import json
import os

from urllib3.exceptions import ProtocolError
from datetime import datetime, timedelta

class TweetJson:
    def __init__(self, text, created_at, public_metrics) -> None:
        self.text = text
        self.created_at = created_at
        self.public_metrics = public_metrics

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    

def writeJson(tweets, start_time):

    day = start_time.split("T")[0]
    time = start_time.split("T")[1].split("Z")[0].replace(":", "-")
    newpath = r'./data/'+day 
    # make a new folder for each day in which every API call is in a new json file
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    with open("./data/"+ day +"/"+ time +".json", "a+", encoding = "utf-8") as json_file:
        json.dump(tweets, json_file ,ensure_ascii=False, indent=2)
        json_file.write("\n")
    
        

def main():
    API_Key = "KWmyvhX0xY50RpO3n533Ryjgo"
    API_Key_Secret = "9I1MLWGRgBWipPk2lNaXeFxBnCjI3E3BGHHg7JnVl8tnqzBqQD"
    Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAEr%2FjQEAAAAAbWNPJPAfjRkIrQMvNjv%2FbulAcLQ%3DgVdGbn90pEFinRVjBBR8D9uaghG6gZrB4BYJYb23wJqD2cgzSR"
    Access_Token = "1593925511536844801-hkAihmhqaGGUI1EuOdfkRFDFNgcTkR"
    Access_Token_Secret = "c0esjuxOmDT5TymcCORkCDfxf0CRpRMaulBmrUJkJRKrP"

    # setup up connection
    client = tweepy.Client(
    consumer_key= API_Key, 
    consumer_secret= API_Key_Secret, 
    bearer_token= Bearer_Token, 
    access_token=Access_Token, 
    access_token_secret=Access_Token_Secret,
    wait_on_rate_limit=True)

    """
        query:  (hier sind suchwörten UND verknüpft)
                "-" Negation
        https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    """
    
    dtformat = '%Y-%m-%dT%H:%M:%SZ'
    start_time_scrappe = (datetime.now() - timedelta(days=7)).strftime(dtformat)
    
    query_result = client.search_recent_tweets(
        # achte bei der query auch darauf dass viele Menschen Wörter flasch schreiben
        query = "-is:retweet -is:reply -is:quote lang:de -liveticker -newsticker (#WM2022 OR #FIFAWorldCup OR FIFA OR WM OR (WM (Katar OR Qatar)) OR ((Fußball OR Fussball) (Qatar OR Katar)))",
        max_results = 100, # limit: 300 requests per 15-minute window
        end_time = start_time_scrappe, #YYYY-MM-DDTHH:mm:ssZ
        tweet_fields = ['created_at','public_metrics'], #[attachments,author_id,context_annotations,conversation_id,created_at,edit_controls,edit_history_tweet_ids,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,organic_metrics,possibly_sensitive,promoted_metrics,public_metrics,referenced_tweets,reply_settings,source,text,withheld]
        # next_token = # get the next tweets 
    )

    tweets_json = {}

    for tweet in query_result.data:
        id = tweet.data['id']
        text = tweet.data['text']
        created_at = tweet.data['created_at']
        public_metrics = tweet.data['public_metrics']
        tweet_json = TweetJson( text, created_at, public_metrics)
        tweets_json[id] = json.loads(tweet_json.toJson())

    writeJson(tweets_json, start_time_scrappe)


if __name__ == '__main__':
    retries = [pow(2,i) for i in range(10)] # Exponential backoff
    while retries:
        try:
            main()
            sys.exit()
        except ConnectionError as e:
            print("Connection error, retrying")
            print(e)
            time.sleep(retries.pop())
        except ProtocolError as e:
            print("Connection error, retrying")
            print(e)
            time.sleep(retries.pop())
