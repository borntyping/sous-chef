"""The create_app() function"""

import chef
import flask

import sous_chef.blueprints

__all__ = ['create_app']


def configure_chef():
    flask.current_app.chef = chef.autoconfigure()
    flask.current_app.chef.set_default()


def create_app():
    app = flask.Flask('sous_chef')
    app.before_first_request(configure_chef)
    app.register_blueprint(sous_chef.blueprints.ui)
    app.register_blueprint(sous_chef.blueprints.api, url_prefix='/api/v0')
    return app
