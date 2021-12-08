from flask import Blueprint
from datetime import datetime, timedelta
from functools import partial
from api.schemas import DashboardTileSchema, DashboardTileDataSchema
from api.utils import jsonify_data, get_json
from api.tweetioc import get_tweetioc_full_ioc

dashboard_api = Blueprint('dashboard', __name__)
get_dashboardtile_form_params = partial(get_json, schema=DashboardTileSchema())
get_dashboardtiledata_form_params = partial(get_json, schema=DashboardTileDataSchema())


def set_valid_time():
    return {
        'start_time': str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
        'end_time': str((datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    }
def set_observed_time(timeframe_in_sec):
    return {
        'start_time': str((datetime.now() - timedelta(seconds=timeframe_in_sec)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
        'end_time': str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    }

def create_tile_data(data_json):
    valid_time = set_valid_time()
    observed_time = set_observed_time(604800)
    data = []
    data.append('[Twitter IOC Hunter](http://tweettioc.com/)')
    data.append('&nbsp;')
    data.append('Daily Tweet from IOC Hunter')
    data.append('| Timestamp | &nbsp; | Twitter Account | &nbsp; | IOC | &nbsp; | Tweet | &nbsp; | Hashtags | &nbsp; | Link |')
    data.append('| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |')
    for tweet in reversed(data_json):
        ioc = []
        for ip in tweet['ip']:
            ioc.append(ip)
        for md5 in tweet['md5']:
            ioc.append(md5)
        for sha1 in tweet['sha1']:
            ioc.append(sha1)
        for sha256 in tweet['sha256']:
            ioc.append(sha256)
        for mail in tweet['mail']:
            ioc.append(mail)
        for domain in tweet['domain']:
            ioc.append(domain)
        for url in tweet['url']:
            ioc.append(url)
        ioc = ' '.join(ioc)
        hashtags = ' '.join(tweet['tweet']['hashtags'])
        account_url = 'http://twitter.com/{}'.format(tweet['tweet']['user'])
        timestamp = datetime.utcfromtimestamp(tweet['tweet']['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        line = '| {} | | [{}]({}) | | {} | | {} | | {} | | {} |'.format(timestamp ,tweet['tweet']['user'], account_url, ioc, tweet['tweet']['tweet'].replace("\n", " ").replace("|", " "), hashtags,tweet['tweet']['link']  )
        data.append(line)

    data = {
        'valid_time': valid_time,
        'hide_legend': True,
        'cache_scope': 'org',
        'observed_time': observed_time,
        'data': data
    }
    return data

def get_tile(description, tags, tile_type, title, tile_id):
    return {
        'description': description,
        'periods': [
            'last_7_days'
        ],
        'tags': tags,
        'type': tile_type,
        'short_description': description,
        'title': title,
        'default_period': 'last_7_days',
        'id': tile_id
    }

@dashboard_api.route('/tiles', methods=['POST'])
def tiles():
    data = []
    title = 'Get the daily tweets from Twitter IOC Hunter'
    tags = ['twitter']
    tile_type = 'markdown'
    description = 'Show the recent tweets from Twitter IOC Hunter'
    tile_id = 'twitter_ioc_hunter'
    data.append(get_tile(description, tags, tile_type, title, tile_id))

    return jsonify_data(data)

@dashboard_api.route('/tiles/tile', methods=['POST'])
def tile():
    return jsonify_data({})

@dashboard_api.route('/tiles/tile-data', methods=['POST'])
def tile_data():
    data = []
    params = get_dashboardtiledata_form_params()
    if 'twitter_ioc_hunter' in params['tile_id']:
        data_json = get_tweetioc_full_ioc()
        data = create_tile_data(data_json)
    else:
        return jsonify_data(data)

    return jsonify_data(data)
