"""The create_app() function"""

import chef
import flask

import sous_chef.blueprints

__all__ = ['create_app']


def configure_chef():
    flask.current_app.chef = chef.autoconfigure()
    flask.current_app.chef.set_default()


def get_chef_environments():
    flask.current_app.chef_environments = sorted(chef.Environment.list())


def create_app():
    app = flask.Flask('sous_chef')
    app.config['SECRET_KEY'] = 'default-secret-key'
    app.before_first_request(configure_chef)
    app.before_first_request(get_chef_environments)
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
