"""Flask blueprints for sous-chef"""

import flask
import chef

__all__ = ['api']

ui = flask.Blueprint('ui', __name__, template_folder='templates/ui')


@ui.route('/')
@ui.route('/roles')
def role_index():
    roles = sorted(chef.Role.list())
    return flask.render_template('role_index.html', roles=roles)


@ui.route('/roles/<string:name>')
def role(name):
    role = chef.Role(name)
    nodes = chef.Search('node', 'roles:{} AND chef_environment:{}'.format(
        role.name, 'production'))
    return flask.render_template('role.html', role=role, nodes=nodes)

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

about = flask.Blueprint('about', __name__, template_folder='templates/about')


@about.route('/')
@about.route('/readme')
def readme():
    return flask.render_template('readme.html')


@about.route('/urls')
@about.route('/rules')
def rules():
    rules = flask.current_app.url_map.iter_rules()
    rules = sorted(rules, key=lambda r: r.rule)
    return flask.render_template('rules.html', rules=rules)
