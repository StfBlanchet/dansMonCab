from flask import Flask
from dansMonCab.config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

from dansMonCab import dansmoncab