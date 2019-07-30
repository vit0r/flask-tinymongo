"""
MOCK database API
"""

from flask import Flask
from blueprints import bp
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(16)
app.register_blueprint(bp)
