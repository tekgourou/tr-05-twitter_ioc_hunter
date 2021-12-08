from functools import partial
from datetime import datetime, timedelta
from api.schemas import ObservableSchema
from api.utils import get_json, jsonify_data, format_docs  # MODIFY THIS LINE
from flask import Blueprint, current_app, jsonify, g
from api.tweetioc import search_ioc
from api.sighting import create_sighting



def group_observables(relay_input):
    result = []
    for observable in relay_input:
        o_value = observable['value']
        o_type = observable['type'].lower()

        if o_type in current_app.config['CCT_OBSERVABLE_TYPES']:
            obj = {'type': o_type, 'value': o_value}
            if obj in result:
                continue
            result.append(obj)
    return result

def build_input_api(observables):
    for observable in observables:
        o_value = observable['value']
        o_type = observable['type'].lower()
        if current_app.config['CCT_OBSERVABLE_TYPES'][o_type].get('sep'):
            o_value = o_value.split(
                current_app.config['CCT_OBSERVABLE_TYPES'][o_type]['sep'])[-1]
            observable['value'] = o_value
    return observables

enrich_api = Blueprint('enrich', __name__)
get_observables = partial(get_json, schema=ObservableSchema(many=True))

@enrich_api.route('/deliberate/observables', methods=['POST'])
def deliberate_observables():
    relay_input = get_json(ObservableSchema(many=True))
    observables = group_observables(relay_input)
    if not observables:
        return jsonify_data({})
    observables = build_input_api(observables)
    data = {}  # Let's create a data directory to be sent back to Threat Response
    g.verdicts = []  # Let's create a list into which we will store valid verdicts data results for every observables
    for observable in observables:
        o_value = observable['value']
        o_type = observable['type'].lower()
        try:
            tweets_data = search_ioc(o_value)
            if tweets_data['count'] >= 1:
                start_time = datetime.utcnow()
                end_time = start_time + timedelta(weeks=1)
                valid_time = {
                    'start_time': start_time.isoformat() + 'Z',
                    'end_time': end_time.isoformat() + 'Z',
                }
                verdict = {
                    'type': 'verdict',
                    'observable': {'type': o_type, 'value': o_value},
                    'disposition': 3,
                    'disposition_name': 'Suspicious',
                    'valid_time': valid_time
                    }
                g.verdicts.append(verdict)
                if g.verdicts:
                    data['verdicts'] = format_docs(g.verdicts)
        except:
            return ({})

    result = {'data': data}

    return jsonify(result)


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    g.sightings = []  # Let's create a list into which we will store valid verdicts data results for every observable
    relay_input = get_json(ObservableSchema(many=True))
    observables = group_observables(relay_input)
    data = []
    if not observables:
        return jsonify_data({})
    observables = build_input_api(observables)
    for observable in observables:
        o_value = observable['value']
        o_type = observable['type'].lower()
        try:
            tweets_data = search_ioc(o_value)
            if tweets_data['count'] != 0:
                for tweet in tweets_data['tweets']:
                    sighting = create_sighting(tweet, o_value, o_type)
                    g.sightings.append(sighting)
                    if g.sightings:
                        data['sightings'] = format_docs(g.sightings)

        except:
            return jsonify({})
    result = {'data': data}
    return jsonify(result)

@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    relay_input = get_json(ObservableSchema(many=True))
    observables = group_observables(relay_input)
    data = []
    if not observables:
        return jsonify_data({})
    observables = build_input_api(observables)
    for observable in observables:
        o_value = observable['value']
        o_type = observable['type'].lower()
        try:
            tweets_data = search_ioc(o_value)
            if tweets_data['count'] == 0:
                return ({})
            refer_url = tweets_data['tweets'][0]['tweet']['link']
            refer_tweet = tweets_data['tweets'][0]['tweet']['tweet']
            data.append(
                {
                    'id': 'ref_tweetioc_{}'.format(o_value),
                    'title': f'Link for {o_value} in Twitter',
                    'description': refer_tweet,
                    'url': refer_url,
                    'categories': ['Search', 'tweetioc']
                }
            )
        except:
            return ({})
    return jsonify_data(data)