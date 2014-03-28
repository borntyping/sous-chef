"""Flask blueprints for sous-chef"""

from __future__ import absolute_import

import flask
import chef
import chef.exceptions

from sous_chef.chef import PartialSearch, get_node

__all__ = ['ui']


ui = flask.Blueprint('ui', __name__)


@ui.before_request
def set_chef_api_client():
    """Set the global ChefAPI object as the default for this thread"""
    flask.current_app.chef.set_default()


def get_chef_environment():
    """Return the session's selected chef_environment or the default"""
    if 'chef_environment' in flask.session:
        return flask.session['chef_environment']
    else:
        return flask.current_app.config['DEFAULT_CHEF_ENVIRONMENT']


@ui.before_request
def set_chef_environment():
    """Ensure a list of environments is availible"""
    flask.g.chef_environments = sorted(chef.Environment.list())
    flask.g.chef_environment = get_chef_environment()


# Nodes

def get_nodes(search, keys={}, chef_environment=None):
    environment = chef_environment or flask.g.chef_environment
    search = '{0} AND chef_environment:{1}'.format(search, environment)
    return PartialSearch('node', search, keys=keys)


@ui.route('/', endpoint='home')
@ui.route('/nodes/')
def node_index():
    nodes = get_nodes('name:*', keys=['name', 'chef_environment'])
    return flask.render_template('node_index.html', nodes=nodes)


@ui.route('/nodes/<string:name>')
def node(name):
    return flask.render_template('node.html', node=get_node(name, [
        'chef_environment',
        'roles',
        'run_list',
        'packages'
    ]))


# Roles

@ui.route('/roles/')
def role_index():
    return flask.render_template('role_index.html', roles=chef.Role.list())


@ui.route('/roles/<string:name>')
def role(name):
    return flask.render_template(
        'role.html',
        role=chef.Role(name),
        nodes=get_nodes('roles:' + name))


# Environments

@ui.route('/environments/')
def environment_index():
    return flask.render_template(
        'environment_index.html', environments=chef.Environment.list())


@ui.route('/environments/<string:name>')
def environment(name):
    return flask.render_template(
        'environment.html',
        environment=chef.Environment(name),
        nodes=get_nodes('name:*', chef_environment=name))


@ui.route('/set/environment/<string:name>')
def set_environment(name):
    if name == 'all':
        environment = '*'
    elif name in chef.Environment.list():
        environment = name
    else:
        flask.abort(404)

    flask.session['chef_environment'] = environment
    flask.session.permanent = True

    return flask.redirect(
        flask.request.referrer or flask.url_for('ui.environment', name=name))


# Packages

@ui.route('/packages/<string:type>/<string:name>')
def package(type, name):
    nodes = PartialSearch('node', 'packages_{0}:{1}'.format(type, name), keys={
        'package_version': ['packages', type, name, 'version']
    })
    return flask.render_template(
        'package.html', package_type=type, package_name=name, nodes=nodes)
