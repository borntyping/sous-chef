"""The create_app() function"""

import chef
import flask

import sous_chef.blueprints

__all__ = ['create_app']


def configure_chef():
    chef_api_config = (
        flask.current_app.config['CHEF_URL'],
        flask.current_app.config['CHEF_KEY'],
        flask.current_app.config['CHEF_CLIENT'])

    if all(chef_api_config):
        flask.current_app.chef = chef.ChefAPI(*chef_api_config)
    else:
        flask.current_app.chef = chef.autoconfigure()

    flask.current_app.chef.set_default()
    flask.current_app.chef_environments = sorted(chef.Environment.list())


def create_app():
    app = flask.Flask('sous_chef')

    # Load configuration from defaults and an optional config file
    app.config.from_object('sous_chef.defaults')
    app.config.from_envvar('SOUS_CHEF_SETTINGS', silent=True)

    # Configure chef before the first request
    app.before_first_request(configure_chef)

    # Register blueprints - currently only the user interface
    app.register_blueprint(sous_chef.blueprints.ui)

    return app


def create_debug_app():
    app = create_app()
    app.config['DEBUG'] = True

    # Install the Flask debug toolbar extension, if the package is availible
    try:
        from flask_debugtoolbar import DebugToolbarExtension
    except ImportError:
        pass
    else:
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        DebugToolbarExtension(app)

    return app
