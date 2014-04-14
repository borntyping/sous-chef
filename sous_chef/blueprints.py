"""Flask blueprints for sous-chef"""

from __future__ import absolute_import

import collections

import flask
import chef.exceptions

__all__ = ['ui']

ui = flask.Blueprint('ui', __name__)


@ui.errorhandler(404)
@ui.errorhandler(chef.exceptions.ChefServerNotFoundError)
def not_found(error):
    return flask.render_template('404.html', error=error), 404


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
    if expects(endpoint, 'environment') and flask.g.chef_environment != '*':
        values.setdefault('environment', flask.g.chef_environment)


# Environments

@ui.route('/', endpoint='home')
@ui.route('/environments')
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
    search = {'roles': '*', 'chef_environment': flask.g.chef_environment}
    nodes = flask.current_app.chef.partial_search('node', search, ['roles'])
    roles = set((r for node in nodes for r in node['roles']))
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
    """Returns a single row or raises an error"""
    nodes = flask.current_app.chef.partial_search('node', {
        'chef_environment': flask.g.chef_environment,
        'name': name
    }, keys)

    if not nodes:
        raise chef.exceptions.ChefServerNotFoundError('No rows returned')
    elif len(nodes) > 1:
        raise chef.exceptions.ChefServerNotFoundError('Multiple rows returned')
    else:
        return nodes[0]


@ui.route('/nodes/<string:node>')
def redirect_node(node):
    node = get_node(node)
    return flask.redirect(flask.url_for(
        '.node', node=node['name'], environment=node['chef_environment']))


@ui.route('/<environment>/nodes/<string:node>')
def node(node):
    return flask.render_template('node.html', node=get_node(node, [
        'run_list',
        'role',
        'recipes',
        'packages'
    ]))


# Packages

@ui.route('/packages')
@ui.route('/<environment>/packages')
def packages():
    nodes = flask.current_app.chef.partial_search('node', {
        'packages': '*',
        'chef_environment': flask.g.chef_environment
    }, ['packages'])

    packages = collections.defaultdict(set)

    for node in nodes:
        for package_type in node['packages']:
            for package in node['packages'][package_type]:
                packages[package_type].add(package)

    return flask.render_template(
        'packages/index.html', packages=packages)


@ui.route('/packages/<string:type>')
@ui.route('/<environment>/packages/<string:type>')
def packages_by_type(type):
    nodes = flask.current_app.chef.partial_search('node', {
        'packages_' + type: '*',
        'chef_environment': flask.g.chef_environment
    }, {
        'packages': ['packages', type]
    })
    packages = set((p for node in nodes for p in node['packages']))
    return flask.render_template(
        'packages/index.html', packages=packages, type=type)


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
        'packages/view.html', type=type, name=name, nodes=nodes)
