from flask import (
    Flask,
    jsonify,
    make_response
)
from . import config

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def index():
    return make_response(jsonify({'success': True,
                                  'message': 'Test API connection',
                                  }), 200)


@app.route('/artifactory')
def artifactory():
    return make_response(jsonify({'success': True,
                                  'message': 'Artifactory ROOT',
                                  }), 200)

