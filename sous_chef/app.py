"""The create_app() function"""

from __future__ import absolute_import

import flask

import sous_chef.blueprints
import sous_chef.chef

__all__ = ['create_app']


def create_app():
    app = flask.Flask('sous_chef', instance_relative_config=True)

    # Load configuration from an optional instance config file
    app.config.from_pyfile('config.py')

    # Configure chef before the first request
    app.chef = sous_chef.chef.Chef.from_flask_app(app)

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
        app.config['SECRET_KEY'] = 'debug-secret-key'
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        DebugToolbarExtension(app)

    return app
