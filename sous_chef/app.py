"""The create_app() function"""

import time

import chef
import flask
import flask_debugtoolbar

import sous_chef.blueprints

__all__ = ['create_app']


def get_request_time():
    return '{:.2}s'.format(time.time() - flask.g.request_start_time)


def set_request_time():
    flask.g.request_start_time = time.time()
    flask.g.request_time = get_request_time


def configure_chef():
    flask.current_app.chef = chef.autoconfigure()
    flask.current_app.chef.set_default()


def create_app(*args, **kwargs):
    app = flask.Flask('sous_chef', *args, **kwargs)
    app.before_first_request(configure_chef)
    app.before_request(set_request_time)
    app.register_blueprint(sous_chef.blueprints.ui)
    app.register_blueprint(sous_chef.blueprints.api, url_prefix='/api/v0')

    if app.debug:
        app.config.set_default('SECRET_KEY', 'debug')
        flask_debugtoolbar.DebugToolbarExtension(app)

    return app
