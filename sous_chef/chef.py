"""A wrapper around PyChef to deal with configuration"""

from __future__ import absolute_import

import chef


class FlaskChefAPI(chef.ChefAPI):
    @classmethod
    def configure(cls, app):
        keys = ['CHEF_URL', 'CHEF_KEY', 'CHEF_CLIENT']
        args = [app.config[k] for k in keys]
        return cls(*args) if all(args) else chef.autoconfigure()


class Node(chef.Node):
    @property
    def roles(self):
        return sorted(r[5:-1] for r in self.run_list if r.startswith('role'))
