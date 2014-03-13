"""sous-chef - A small webapp for viewing and searching Chef nodes"""

__version__ = '0.2.0'
__author__ = 'Sam Clements <sam.clements@datasift.com>'
__all__ = ['main', 'create_app']


from sous_chef.app import create_app


def main():
    create_app().run()


def debug():
    from flask_debugtoolbar import DebugToolbarExtension

    app = create_app()
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'debug-secret-key'
    DebugToolbarExtension(app)
    app.run()

if __name__ == '__main__':
    main()
