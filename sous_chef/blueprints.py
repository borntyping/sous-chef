"""Flask blueprints for sous-chef"""

import flask
import chef

__all__ = ['api']

ui = flask.Blueprint('ui', __name__)


class Node(chef.Node):
    @property
    def roles(self):
        return sorted(r[5:-1] for r in self.run_list if r.startswith('role'))


@ui.route('/', endpoint='home')
@ui.route('/roles/')
def roles():
    return flask.render_template(
        'role_index.html', roles=sorted(chef.Role.list()))


@ui.route('/roles/<string:name>')
def role(name):
    role = chef.Role(name)
    nodes = chef.Search('node', 'roles:{} AND chef_environment:{}'.format(
        role.name, 'production'))
    return flask.render_template('role.html', role=role, nodes=nodes)


@ui.route('/nodes/')
def nodes():
    return flask.render_template(
        'node_index.html', nodes=sorted(chef.Node.list()))


@ui.route('/nodes/<string:name>')
def node(name):
    return flask.render_template('node.html', node=Node(name))
