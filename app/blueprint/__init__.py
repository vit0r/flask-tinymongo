"""BP Mock"""

from os import urandom
from flask import Blueprint, request, jsonify
from tinymongo import TinyMongoClient
from pathlib import Path
from hashlib import md5
from json import dumps

bp = Blueprint(name='mock', import_name='bp', url_prefix='/api/mock')

def get_id(data):
  request_str = dumps(data.get('name')).encode()
  hash_md5 = md5(bytes(request_str)).hexdigest()
  return hash_md5

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


@bp.route('/<string:mock_name>/appname/<string:app_name>', methods=['GET'])
def get_mock(mock_name, app_name):    
    db = get_db(app_name)
    mock = db[app_name].find_one({'name': mock_name, 'appName': app_name})
    if mock:
        return jsonify(mock.get('response')), 200
    return jsonify({}), 204


@bp.route('/create', methods=['POST'])
def create_mock():
    request_data = request.get_json()
    app_name = request_data.get('appName')
    db = get_db(app_name)
    request_data['_id'] = get_id(request_data)
    data_id = db[app_name].insert_one(request_data).inserted_id
    if data_id:
        return jsonify({'message': 'CREATED'}), 201
    return jsonify({'message': 'ERROR'}), 406
