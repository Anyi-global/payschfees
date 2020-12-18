import os

SECRET_KEY = os.environ.get('SECRET_KEY') or "ajajajjsjsjajjajaaw333"

#connecting to database
MONGO_URI = os.environ.get('MONGO_URI') or "mongodb+srv://andrew_uche:andrewuche4810@cluster0.fcitc.mongodb.net/IKA?retryWrites=true&w=majority"