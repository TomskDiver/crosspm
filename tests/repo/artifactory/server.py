from flask import request

import os

from flask import (
    Flask,
    jsonify,
    make_response
)
from . import config

app = Flask(__name__)
app.config.from_object(config)
STORAGE = os.path.realpath(os.path.join(os.path.dirname(__file__), 'storage'))


@app.route('/')
def index():
    return make_response(jsonify({'success': True,
                                  'message': 'Test API connection',
                                  }), 200)


@app.route('/artifactory')
@app.route('/artifactory/<path:url>')
def artifactory(url=''):
    full_url = request.url
    status = 404
    if not url:
        status = 200
    else:
        path = os.path.join(STORAGE, *(url.replace('//', '/').split('/')))
        if os.path.exists(path):
            status = 200

    return make_response(jsonify({'success': True,
                                  'uri': full_url,
                                  }), status)


@app.route('/artifactory/api/storage/<path:url>')
def api_storage(url):
    full_url = request.url
    repo = ''
    status = 404
    if not url:
        status = 200
    else:
        path_parts = url.replace('//', '/').split('/')
        repo = path_parts[0]
        path = os.path.join(STORAGE, *path_parts)
        if os.path.exists(path):
            status = 200

        # 'Content-Type': 'application/vnd.org.jfrog.artifactory.storage.FolderInfo+json'
        # 'X-Artifactory-Id': 'bf4860c8cc1a2653:-6a8eb9d8:159f28aa6c2:-8000'

    res = {
        'repo': repo,
        'path': '/aggregator/develop',
        'created': '2015-08-25T17:50:21.387+04:00',
        'createdBy': 'deploy_ci',
        'lastModified': '2015-08-25T17:50:21.387+04:00',
        'modifiedBy': 'deploy_ci',
        'lastUpdated': '2015-08-25T17:50:21.387+04:00',
        'children': [{
            'uri': '/14.0.402',
            'folder': True
        }],
        'uri': full_url
    }

    return make_response(jsonify(res), status)
