"""Flask blueprints for sous-chef"""

from __future__ import absolute_import

import collections
import itertools
import json

import chef.exceptions
import flask
import jinja2.filters

import sous_chef

__all__ = ['ui']

ui = flask.Blueprint('ui', __name__)


def accept_json():
    accept = flask.request.accept_mimetypes.best_match([
        'application/json', 'text/html'])
    return accept == 'application/json' and \
        flask.request.accept_mimetypes[accept] > \
        flask.request.accept_mimetypes['text/html']


def render(template_name, **kwargs):
    if accept_json():
        response = flask.make_response(json.dumps(kwargs))
        response.headers['Content-Type'] = 'application/json'
        return response

    return flask.render_template(template_name, **kwargs)


@ui.errorhandler(404)
@ui.errorhandler(chef.exceptions.ChefServerNotFoundError)
def not_found(error):
    return render('404.html', error=error), 404


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


@ui.context_processor
def metadata():
    return {'sous_chef_version': sous_chef.__version__}


# Chef client wrappers

def partial_search(index, search, keys=None):
    """Shortcut for the chef client partial_search function"""
    return flask.current_app.chef.partial_search(index, search, keys)


def partial_search_nodes(search, keys={}):
    """Uses g.chef_environment and adds useful keys"""
    search.setdefault('chef_environment', flask.g.chef_environment)

    keys = flask.current_app.chef.normalise_keys(keys)
    keys.setdefault('name', ['name'])
    keys.setdefault('chef_environment', ['chef_environment'])

    return partial_search('node', search, keys)


def single_row(results):
    """Returns a single row from a set of results or raises an error"""
    if not results:
        raise chef.exceptions.ChefServerNotFoundError('No matching rows found')
    elif len(results) > 1:
        raise chef.exceptions.ChefServerNotFoundError(
            'Multiple rows returned, expected one')
    return results[0]


# Environments

@ui.route('/', endpoint='home')
@ui.route('/environments')
def environments():
    return render(
        'environments/index.html', environments=flask.g.chef_environments)


@ui.route('/<string:environment>')
@ui.route('/environments/<string:environment>')
def environment():
    environment = flask.current_app.chef.get(
        'environments', flask.g.chef_environment)
    nodes = partial_search_nodes({'name': '*'})
    return render(
        'environments/view.html', environment=environment, nodes=nodes)


# Roles

@ui.route('/roles')
@ui.route('/<environment>/roles')
def roles():
    nodes = partial_search_nodes({'roles': '*'}, ['roles'])
    roles = sorted(set((r for node in nodes for r in node['roles'])))
    return render('roles/index.html', roles=roles)


@ui.route('/roles/<string:role>')
@ui.route('/<environment>/roles/<string:role>')
def role(role):
    nodes = partial_search_nodes({'roles': role})
    role = flask.current_app.chef.get('roles', role)
    return render('roles/view.html', role=role, nodes=nodes)


# Nodes

@ui.route('/nodes')
@ui.route('/<environment>/nodes')
def nodes():
    return render(
        'nodes/index.html', nodes=partial_search_nodes({}))


@ui.route('/nodes/<string:node>')
def redirect_node(node):
    node = single_row(partial_search_nodes({'name': node}))
    return flask.redirect(flask.url_for(
        '.node', node=node['name'], environment=node['chef_environment']))


@ui.route('/<environment>/nodes/<string:node>')
def node(node):
    node = single_row(partial_search_nodes({'name': node}, [
        'run_list',
        'platform',
        'platform_version',
        'tags',
        'recipes',
        'packages'
    ]))
    return render('nodes/view.html', node=node)


# Packages

def group_nodes_by_package_version(nodes):
    def version(node, sep='-', unknown='Unknown'):
        identity = list()
        identity.append(node['package_details'].get('version', None))
        identity.append(node['package_details'].get('release', None))
        return sep.join(filter(lambda x: x is not None, identity)) or unknown
    # Group the packages by the version
    packages = itertools.groupby(sorted(nodes, key=version), version)
    # Use jinja2's GroupTuple to match the groupby filter
    return map(jinja2.filters._GroupTuple, packages)


@ui.route('/packages')
@ui.route('/<environment>/packages')
def packages_by_type():
    nodes = partial_search_nodes({'packages': '*'}, ['packages'])

    packages = collections.defaultdict(set)
    for node in nodes:
        for package_type in node['packages']:
            for package in node['packages'][package_type]:
                packages[package_type].add(package)

    return render(
        'packages/index_by_type.html', packages=packages)


@ui.route('/packages/<string:type>')
@ui.route('/<environment>/packages/<string:type>')
def packages_for_type(type):
    nodes = partial_search_nodes(
        {'packages_' + type: '*'}, {'packages': ['packages', type]})
    packages = sorted(set((p for node in nodes for p in node['packages'])))
    return render(
        'packages/index_for_type.html', packages=packages, type=type)


@ui.route('/packages/<string:type>/<string:name>')
@ui.route('/<environment>/packages/<string:type>/<string:name>')
def package(type, name):
    nodes = partial_search_nodes(
        {'packages_{0}_{1}'.format(type, name): '*'},
        {'package_details': ['packages', type, name]})
    return render(
        'packages/view.html', type=type, name=name, nodes=nodes,
        packages_by_version=group_nodes_by_package_version(nodes))
