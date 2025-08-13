from flask import Flask
from os import environ
import logging
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    
    load_dotenv()
    
    # Configure database from environment variables
    app.config['DB_CONFIG'] = {
        'host': environ.get('DB_HOST'),
        'port': environ.get('DB_PORT'),
        'database': environ.get('DB_NAME'),
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASSWORD')
    }
    app.config['DB_SCHEMA'] = environ.get('DB_SCHEMA')

    from .blueprints.playlists.playlists import playlists
    from .blueprints.main.main import main
    from .blueprints.top_playlists.top_playlists import top_playlists

    app.register_blueprint(playlists, url_prefix='/playlists')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(top_playlists, url_prefix='/top-playlists')

    return app