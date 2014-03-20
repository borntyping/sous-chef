"""Flask blueprints for sous-chef"""

from __future__ import absolute_import

import flask
import chef

import sous_chef.chef

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
    return flask.render_template(
        'node_index.html', nodes=chef.Search('node'))


@ui.route('/nodes/<string:name>')
def node(name):
    return flask.render_template(
        'node.html', node=sous_chef.chef.Node(name))


# Roles

@ui.route('/roles/')
def role_index():
    return flask.render_template(
        'role_index.html', roles=sorted(chef.Role.list()))


@ui.route('/roles/<string:name>')
def role(name):
    return flask.render_template(
        'role.html',
        role=chef.Role(name),
        nodes=chef.Search('node', 'role:{0}'.format(name)))


@ui.route('/roles/<string:name>/<string:environment>')
def role_in_environment(name, environment):
    role = chef.Role(name)
    nodes = chef.Search('node', 'role:{0} AND chef_environment:{}'.format(
        name, environment))
    return flask.render_template('role.html', role=name, nodes=nodes)


# Environments

@ui.route('/environments/')
def environment_index():
    return flask.render_template(
        'environment_index.html', environments=sorted(chef.Environment.list()))


@ui.route('/environments/<string:name>')
def environment(name):
    return flask.render_template(
        'environment.html',
        environment=chef.Environment(name),
        nodes=chef.Search('node', 'chef_environment:{0}'.format(name)))


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
