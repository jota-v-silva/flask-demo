import os
import logging
from flask import Flask
from logging.handlers import RotatingFileHandler
from . import app_bp
from .sqlite_handler import SQLiteHandler


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register blueprints
    app.register_blueprint(app_bp.bp)
    
    return app

# Entry point for standard python command
# python -m app
if __name__ == '__main__':
    app = create_app()
    
    sqlite_handler = SQLiteHandler('out/test_log.db', 'LOG_MESSAGES')
    sqlite_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(sqlite_handler)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    log.addHandler(sqlite_handler)
    
    app.run(host='0.0.0.0', port=5555, debug=True)

