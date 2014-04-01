"""Flask blueprints for sous-chef"""

from __future__ import absolute_import

import flask
import chef.exceptions

__all__ = ['ui']

ui = flask.Blueprint('ui', __name__)


@ui.errorhandler(chef.exceptions.ChefServerNotFoundError)
def not_found_error(error):
    return "The Chef Server could not find the requested item", 404


@ui.before_request
def get_chef_environments():
    """Ensure a list of environments is availible"""
    flask.g.chef_environments = flask.current_app.chef.get('environments')


@ui.url_value_preprocessor
def pop_chef_environment(endpoint, values):
    """Set the current environment, defaulting to * for all environments"""
    flask.g.chef_environment = values.pop('environment', '*')


@ui.url_defaults
def put_chef_environment(endpoint, values):
    """Set a default environment in calls to url_for"""
    expects = flask.current_app.url_map.is_endpoint_expecting
    if expects(endpoint, 'environment'):
        values.setdefault('environment', flask.g.chef_environment)


# Environments

@ui.route('/', endpoint='home')
@ui.route('/environments/')
def environments():
    return flask.render_template(
        'environments.html', environments=flask.g.chef_environments)


@ui.route('/<string:environment>')
@ui.route('/environments/<string:environment>')
def environment():
    environment = flask.current_app.chef.get(
        'environments', flask.g.chef_environment)
    nodes = flask.current_app.chef.partial_search(
        'node', {'chef_environment': flask.g.chef_environment})
    return flask.render_template(
        'environment.html', environment=environment, nodes=nodes)


# Roles

@ui.route('/roles')
@ui.route('/<environment>/roles')
def roles():
    roles = flask.current_app.chef.get('roles').keys()
    return flask.render_template('roles.html', roles=roles)


@ui.route('/roles/<string:role>')
@ui.route('/<environment>/roles/<string:role>')
def role(role):
    _role = flask.current_app.chef.get('roles', role)
    nodes = flask.current_app.chef.partial_search('node', {
        'chef_environment': flask.g.chef_environment,
        'roles': role
    })
    return flask.render_template('role.html', role=_role, nodes=nodes)


# Nodes

@ui.route('/nodes')
@ui.route('/<environment>/nodes')
def nodes():
    nodes = flask.current_app.chef.partial_search('node', {
        'chef_environment': flask.g.chef_environment
    })
    return flask.render_template('nodes.html', nodes=nodes)


def get_node(name, keys={}):
    nodes = list(flask.current_app.chef.partial_search('node', {
        'chef_environment': flask.g.chef_environment,
        'name': name
    }, keys))

    if len(nodes) != 1:
        raise chef.exceptions.ChefServerNotFoundError()

    return nodes[0]


@ui.route('/nodes/<string:node>')
def redirect_node(node):
    node = flask.current_app.chef.node(node)
    return flask.redirect(flask.url_for(
        '.node', node=node['name'], environment=node['chef_environment']))


@ui.route('/<environment>/nodes/<string:node>')
def node(node):
    node = flask.current_app.chef.node(node, [
        'run_list',
        'role',
        'recipes',
        'packages'
    ])
    return flask.render_template('node.html', node=node)


# Packages

@ui.route('/packages/<string:type>/<string:name>')
@ui.route('/<environment>/packages/<string:type>/<string:name>')
def package(type, name):
    nodes = flask.current_app.chef.partial_search('node', {
        'chef_environment': flask.g.chef_environment,
        'packages_' + type: name
    }, {
        'package_version': ['packages', type, name, 'version']
    })
    return flask.render_template(
        'package.html', package_type=type, package_name=name, nodes=nodes)
