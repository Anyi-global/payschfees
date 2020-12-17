#####################################################################################
########################   LIBRARIES  ################################################
#######################################################################################
from flask import Flask
from flask_pymongo import PyMongo
import os
from app.config import MONGO_URI, SECRET_KEY
from flask_restful import Api


#####################################################################################
########################   INITIALIZATION  ################################################
#######################################################################################
# Initializing Flask
app = Flask (__name__)

#app configuration
app_settings = os.environ.get(
    'APP_SETTINGS'
    'app.config'
) 
app.config.from_object(app_settings)

#initializing PyMongo
mongo = PyMongo(app, MONGO_URI)

#init Api app
api = Api(app)

from app import view, payapi