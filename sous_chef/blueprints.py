"""Flask blueprints for sous-chef"""

import flask
import chef

__all__ = ['api']

ui = flask.Blueprint('ui', __name__)


class Node(chef.Node):
    @property
    def roles(self):
        return sorted(r[5:-1] for r in self.run_list if r.startswith('role'))


@ui.route('/')
@ui.route('/roles/')
def role_index():
    return flask.render_template(
        'role_index.html', roles=sorted(chef.Role.list()))


@ui.route('/roles/<string:name>')
def role(name):
    role = chef.Role(name)
    nodes = chef.Search('node', 'roles:{} AND chef_environment:{}'.format(
        role.name, 'production'))
    return flask.render_template('role.html', role=role, nodes=nodes)


@ui.route('/nodes/')
def node_index():
    return flask.render_template(
        'node_index.html', nodes=sorted(chef.Node.list()))


@ui.route('/nodes/<string:name>')
def node(name):
    return flask.render_template('node.html', node=Node(name))


api = flask.Blueprint('api', __name__)


@api.route('/nodes')
def nodes():
    return flask.jsonify(nodes=sorted(chef.Node.list()))


@api.route('/nodes/<string:role>')
def nodes_by_role(role):
    nodes = chef.Search('node', 'roles:{}'.format(role))
    return flask.jsonify(nodes=[node.object.name for node in nodes])


@api.route('/roles')
def roles():
    return flask.jsonify(roles=sorted(chef.Role.list()))
