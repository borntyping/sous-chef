"""A wrapper around PyChef to deal with configuration"""

from __future__ import absolute_import

import collections
import urllib # urllib.parse for Python 3

import chef


class FlaskChefAPI(chef.ChefAPI):
    @classmethod
    def configure(cls, app):
        keys = ['CHEF_URL', 'CHEF_KEY', 'CHEF_CLIENT']
        args = [app.config[k] for k in keys]
        return cls(*args) if all(args) else chef.autoconfigure()


class PartialSearch(collections.Iterable):
    """A class similar to the existing Search class in PyChef, using Chef's
    partial search API - this only returns the requested keys and is much
    faster than a full search."""

    url = '/search'

    def __init__(self, index, q='*:*', keys={}, rows=1000, start=0, api=None):
        self.name = index
        self.keys = keys
        self.api = api or chef.api.ChefAPI.get_global()

        self._args = dict(q=q, rows=rows, start=start)
        self.url = '/{url}/{index}?{args}'.format(
            url=self.__class__.url,
            index=index,
            args=urllib.urlencode(dict(q=q, rows=rows, start=start)))

    @staticmethod
    def keys_from_object(keys):
        # Coerce lists of dotted attibutes to a dict
        if isinstance(keys, list):
            keys = [key.split('.') for key in keys]
            keys = dict((key[0], key) for key in keys)

        # Always return the name and chef environment
        keys.setdefault('name', ['name'])
        keys.setdefault('chef_environment', ['chef_environment'])

        return keys

    @property
    def body(self):
        return self.keys_from_object(self.keys)

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = self.api.api_request('POST', self.url, data=self.body)
        return self._data

    def __iter__(self):
        for row in self.data['rows']:
            yield row['data']

    def __len__(self):
        return len(self.data['rows'])

    def __getitem__(self, value):
        return self.data['rows'][value]


def get_node(name, keys):
    """Returns a single node using Chef partial search"""
    nodes = PartialSearch('node', 'name:' + name, keys=keys)
    if not nodes:
        raise chef.exceptions.ChefError('No node found')
    elif len(nodes) > 1:
        raise chef.exceptions.ChefError('Too many results returned')
    else:
        return nodes[0]['data']
