import flask
import logging

from flask import request
from utils import validate_post_data, error_response, success_response, process_data, get_history

app = flask.Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return 'AI Text Processing Service'

@app.route('/history', methods=['GET'])
def history():
    try:
        ret = get_history()
        return success_response('History received', ret)
    except Exception as e:
        return error_response(str(e))

@app.route('/process', methods=['POST'])
def process():
    try:
        post_data = request.get_json()
        is_valid, error_msg = validate_post_data(post_data)
        if not is_valid:
            return error_response(error_msg)
        ret = process_data(post_data['text'])
        return success_response('Data received', ret)
    except Exception as e:
        return error_response(str(e))

if __name__ == '__main__':
    app.run()