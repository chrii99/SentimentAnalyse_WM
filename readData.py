import json
import os
import time
from datetime import datetime, timedelta
from operator import itemgetter
import numpy as np
import pandas as pd

def dateConvertToTimestamp(date_str):
    return time.mktime(datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())

def readJson(path):
    f = open(path)
    jsonFile = json.load(f)
    f.close()

    return jsonFile

def writeJson(tweets:dict):

    newpath = r'./data/' 
    # make a new folder for each day in which every API call is in a new json file
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    with open("./data/Tweets_WM2022.json", "a+", encoding = "utf-8") as json_file:
        json.dump(tweets, json_file ,ensure_ascii=False, indent=2)
        json_file.write("\n")

def getTweetsFromTo(Start_Date, End_Date) -> pd.DataFrame:
    dtformat_folder = '%Y-%m-%d'

    data = dict()

    tweet_count = 0

    # Wm Dauer von 20.11 bis 18.12 -> 29 Tage
    days = (End_Date - Start_Date).days + 1

    for i in range(days):
        folder = (Start_Date + timedelta(days=i)).strftime(dtformat_folder)
        
        path = r'./data/'+folder+'/'

        for root, dirs, files in os.walk(path):
            sortedFiles = sorted(files)
            for file in sortedFiles:
                tweets = readJson('./data/'+folder+'/'+file)
                data.update(tweets) #if item doesn't exist, ist will be added

    tweet_count = len(data)

    #order from oldest first to latest last
    data_sorted = dict(sorted(data.items(), key=lambda item: item[1]['created_at']))

    #create pandas Dataframe 
    data_from_dict = pd.DataFrame({
        'text':np.array([tweets['text'] for tweet_id, tweets in data_sorted.items()]),
        'date':np.array([tweets['created_at'] for tweet_id, tweets in data_sorted.items()]),
        'retweet_count':np.array([tweets['public_metrics']['retweet_count'] for tweet_id, tweets in data_sorted.items()]),
        'reply_count':np.array([tweets['public_metrics']['reply_count'] for tweet_id, tweets in data_sorted.items()]),
        'like_count':np.array([tweets['public_metrics']['like_count'] for tweet_id, tweets in data_sorted.items()]),
        'qoute_count':np.array([tweets['public_metrics']['quote_count'] for tweet_id, tweets in data_sorted.items()])
        })

    return data_from_dict

print("END")