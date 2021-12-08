import requests
import json
from datetime import datetime, timedelta


def get_tweetioc_full_ioc():
    end_day = str(datetime.now().strftime("%Y-%m-%d"))
    start_day = str((datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))
    url = "http://www.tweettioc.com/v1/tweets/{}/{}/full".format(start_day,end_day)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload).text
    return json.loads(response)

def search_ioc(obs_value):
    tweets = get_tweetioc_full_ioc()
    tweets_data = {}
    tweets_short_list = []
    count = 0
    for tweet in reversed(tweets):
        tweet = json.dumps(tweet)
        if obs_value in tweet:
            count = count+1
            tweets_short_list.append(json.loads(tweet))

    tweets_data['count'] = count
    tweets_data['tweets'] = tweets_short_list
    return tweets_data




