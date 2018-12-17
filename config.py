import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'UMGBQnIFXbyaPmSCXRroVLJMTIrNaeWz'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_RCONPASSWORD = 'area51'
    SERVER_ADDRESS = "127.0.0.1"
    SERVER_PORT = 28960
    SERVER_RCONPASSWORD = "password"
    IMAGES_PATH = os.path.join(basedir, '/static/images/')
