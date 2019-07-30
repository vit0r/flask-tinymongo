"""
MOCK database API
"""

from flask import Flask
from .blueprint import bp
from os import urandom

app = Flask(__name__, static_url_path='static')
app.secret_key = urandom(16)
app.register_blueprint(bp)
