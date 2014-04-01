"""Flask blueprints for sous-chef"""

from __future__ import absolute_import

import flask
import chef.exceptions

__all__ = ['home', 'environment']

home = flask.Blueprint('home', __name__)


@home.route('/')
@home.route('/', endpoint='home')
def environments():
    environments = flask.current_app.chef.get('environments')
    return flask.render_template(
        'environments.html', environments=environments)


environment = flask.Blueprint(
    'environment', __name__, url_prefix='/<string:environment>')


@environment.errorhandler(chef.exceptions.ChefServerNotFoundError)
def not_found_error(error):
    return "The Chef Server could not find the requested item", 404


@environment.url_defaults
def put_chef_environment(endpoint, values):
    if 'environment' not in values:
        values['environment'] = flask.g.chef_environment


@environment.url_value_preprocessor
def pop_chef_environment(endpoint, values):
    flask.g.chef_environment = values.pop('environment')


@environment.before_request
def get_chef_environments():
    """Ensure a list of environments is availible"""
    flask.g.chef_environments = flask.current_app.chef.get('environments')


# Environments

@environment.route('/', endpoint='home')
def environment_home():
    environment = flask.current_app.chef.get(
        'environments', flask.g.chef_environment)
    nodes = flask.current_app.chef.partial_search(
        'node', {'chef_environment': flask.g.chef_environment})
    return flask.render_template(
        'environment.html', environment=environment, nodes=nodes)


# Roles

@environment.route('/roles')
def roles():
    roles = flask.current_app.chef.get('roles').keys()
    return flask.render_template('roles.html', roles=roles)


@environment.route('/roles/<string:role>')
def role(role):
    _role = flask.current_app.chef.get('roles', role)
    nodes = flask.current_app.chef.partial_search('node', {
        'chef_environment': flask.g.chef_environment,
        'roles': role
    })
    return flask.render_template('role.html', role=_role, nodes=nodes)


# Nodes

@environment.route('/nodes')
def nodes():
    nodes = flask.current_app.chef.partial_search('node', {
        'chef_environment': flask.g.chef_environment
    })
    return flask.render_template('nodes.html', nodes=nodes)


@environment.route('/nodes/<string:node>')
def node(node):
    nodes = flask.current_app.chef.partial_search('node', {
        'chef_environment': flask.g.chef_environment,
        'name': node
    }, ['run_list', 'role', 'recipes', 'packages'])

    node = list(nodes)[0]

    return flask.render_template('node.html', node=node)


# Packages

@environment.route('/packages/<string:type>/<string:name>')
def package(type, name):
    nodes = flask.current_app.chef.partial_search('node', {
        'chef_environment': flask.g.chef_environment,
        'packages_' + type: name
    }, {
        'package_version': ['packages', type, name, 'version']
    })
    return flask.render_template(
        'package.html', package_type=type, package_name=name, nodes=nodes)
