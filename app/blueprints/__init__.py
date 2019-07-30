"""BP Mock"""

from os import urandom
from flask import Blueprint, request, jsonify
from tinymongo import TinyMongoClient
from pathlib import Path

bp = Blueprint(name='mock', import_name='bp', url_prefix='/api/mock')


def get_mocks_dir():
    mocks_dir = Path(bp.root_path, 'mocks')
    if not Path.exists(mocks_dir):
        Path.mkdir(mocks_dir, parents=True)
    return mocks_dir


def get_db(app_name):
    if not isinstance(app_name, str):
        return jsonify({'message': 'invalid name for app'}), 400
    mocks_dir = get_mocks_dir()
    connection = TinyMongoClient(
        foldername=mocks_dir.resolve())
    return connection[app_name]


@bp.route('/', methods=['GET', 'CUSTOM'])
def get_mock():
    data = request.get_json()
    db = get_db()
    mock = db.find(data).cursordat
    if mock:
        return jsonify(mock), 200
    return jsonify({}), 204


@bp.route('/create', methods=['POST'])
def create_mock():
    data = request.get_json()
    app_name = data.get('appName')
    db = get_db(app_name)
    data_id = db[app_name].insert_one(data).inserted_id
    if data_id:
        return jsonify({'message': 'CREATED'}), 201
    return jsonify({'message': 'ERROR'}), 406
