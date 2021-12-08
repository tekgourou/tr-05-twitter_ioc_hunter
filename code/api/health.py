from flask import Blueprint
from api.utils import jsonify_data
from api.tweetioc import get_tweetioc_full_ioc
health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    try:
        get_tweetioc_full_ioc()
        return jsonify_data({'status': 'ok'})
    except:
        return jsonify_data({})


