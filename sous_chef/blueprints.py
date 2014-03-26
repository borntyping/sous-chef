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


# Nodes

@ui.route('/', endpoint='home')
@ui.route('/nodes/')
def node_index():
    nodes = PartialSearch('node', keys=['name', 'chef_environment'])
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
        nodes=PartialSearch('node', 'roles:' + name))


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
        nodes=PartialSearch('node', 'chef_environment:' + name))


# Packages

@ui.route('/packages/<string:type>/<string:name>')
def package(type, name):
    nodes = PartialSearch('node', 'packages_{0}:{1}'.format(type, name), keys={
        'package_version': ['packages', type, name, 'version']
    })
    return flask.render_template(
        'package.html', package_type=type, package_name=name, nodes=nodes)


# def current_envionment():
#     if not 'chef_environment' in flask.session:
#         flask.session['chef_environment'] = flask.current_app.config.get(
#             'DEFAULT_CHEF_ENVIRONMENT', '_default')
#     return flask.session['chef_environment']

# @ui.before_request
# def set_environment_variables():
#     """Ensure a list of environments is availible"""
#     flask.g.chef_environments = sorted(chef.Environment.list())
#     flask.g.chef_environment = current_envionment()

# @ui.route('/environments/<string:name>/select')
# def select_environment(name):
#     if name in flask.g.chef_environments:
#         flask.session['chef_environment'] = name
#         flask.session.permanent = True
#     return flask.redirect(flask.request.referrer or flask.url_for('ui.home'))
