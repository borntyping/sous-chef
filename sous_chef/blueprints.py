"""Flask blueprints for sous-chef"""

import flask
import chef

__all__ = ['ui']

ui = flask.Blueprint('ui', __name__)


def default_environment():
    return flask.current_app.config.get('DEFAULT_CHEF_ENVIRONMENT', '_default')


def current_envionment():
    return flask.session.get('chef_environment', default_environment())


def search_nodes(**kwargs):
    kwargs.setdefault('chef_environment', current_envionment())
    search = ' AND '.join('{0}:{1}'.format(k, v) for k, v in kwargs.items())
    return chef.Search('node', search)


def search_node_names(**kwargs):
    return sorted(row['name'] for row in search_nodes(**kwargs))


class Node(chef.Node):
    @property
    def roles(self):
        return sorted(r[5:-1] for r in self.run_list if r.startswith('role'))


@ui.route('/', endpoint='home')
@ui.route('/roles/')
def roles():
    return flask.render_template('roles.html', roles=sorted(chef.Role.list()))


@ui.route('/roles/<string:name>')
def role(name):
    role = chef.Role(name)
    nodes = search_node_names(role=role.name)
    return flask.render_template('role.html', role=role, nodes=nodes)


@ui.route('/nodes/')
def nodes():
    return flask.render_template('nodes.html', nodes=search_node_names())


@ui.route('/nodes/<string:name>')
def node(name):
    return flask.render_template('node.html', node=Node(name))


@ui.before_request
def set_environment_variables():
    flask.g.chef_environments = flask.current_app.chef_environments
    flask.g.chef_environment = current_envionment()


@ui.route('/environments/')
def environments():
    return flask.render_template(
        'environments.html', environments=sorted(chef.Environment.list()))


@ui.route('/environments/<string:name>')
def environment(name):
    environment = chef.Environment(name)
    nodes = search_node_names(chef_environment=environment.name)
    return flask.render_template(
        'environment.html', environment=environment, nodes=nodes)


@ui.route('/environments/<string:name>/select')
def select_environment(name):
    if name in flask.g.chef_environments:
        flask.session['chef_environment'] = name
        flask.session.permanent = True
    return flask.redirect(flask.request.referrer or flask.url_for('ui.home'))
