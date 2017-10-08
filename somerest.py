# coding=utf-8
import logging

import datetime
import os

from flask import Flask
from flask_compress import Compress
from flask_cors import CORS
from flask_restplus import Api
from flask_caching import Cache


# set up logging
logging.basicConfig(format='%(asctime)s [%(levelname)s, %(module)s] %(message)s', level=logging.DEBUG)
fh = logging.FileHandler('logs/%s_%05d.log' % (datetime.datetime.now().strftime('%Y%m%d_%H%M%S'), os.getpid()))
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s, %(module)s] %(message)s'))
logger = logging.getLogger()
logger.addHandler(fh)
app = Flask(__name__)

# add compression
Compress(app)

# add a secret key to allow session storage
app.secret_key = "somesecretkey"

# add caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# register API
api = Api(app, version='1', title=u'Some-title', description='some',
           validate=True)

# allow CORS
CORS(app)

# configuration
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

from app import views
