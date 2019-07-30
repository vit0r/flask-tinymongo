"""BP Mock"""

from os import urandom
from flask import Blueprint, request, jsonify
from tinymongo import TinyMongoClient
from pathlib import Path
from hashlib import md5
from json import dumps

bp = Blueprint(name='mock', import_name='bp', url_prefix='/api/mock')


def get_mocks_dir():
    from os import environ
    dir_d = bp.root_path + '/mocks'
    mocks_dir = Path(environ.get('APPLICATION_ROOT_MOCKS', dir_d))
    if not Path.exists(mocks_dir):
        Path.mkdir(mocks_dir, parents=True)
    return mocks_dir


def get_db(app_name):
    if not isinstance(app_name, str):
        return jsonify({'message': 'invalid name for app'}), 400
    mocks_dir = get_mocks_dir()
    connection = TinyMongoClient(foldername=mocks_dir.resolve())
    return connection[app_name]

def get_id(data):
  request_str = dumps(data).encode()
  hash_md5 = md5(bytes(request_str)).hexdigest()
  return hash_md5

@bp.route('/', methods=['GET', 'CUSTOM'])
def get_mock():
    data = request.get_json()
    app_name = data.get('appName')
    db = get_db(app_name)
    mock = db[app_name].find_one({'_id': get_id(data)})
    if mock:
        return jsonify(mock.get('response')), 200
    return jsonify({}), 204


@bp.route('/create', methods=['POST'])
def create_mock():
    data = request.get_json()
    app_name = data.get('appName')
    data['_id'] = get_id(data)    
    db = get_db(app_name)
    data_id = db[app_name].insert_one(data).inserted_id
    if data_id:
        return jsonify({'message': 'CREATED'}), 201
    return jsonify({'message': 'ERROR'}), 406
