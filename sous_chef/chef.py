"""A wrapper around PyChef to deal with configuration"""

from __future__ import absolute_import

import collections
import urllib  # urllib.parse for Python 3

import chef.api
import chef.exceptions


class Chef(object):
    @classmethod
    def from_flask_app(cls, app):
        config_keys = ('CHEF_URL', 'CHEF_KEY', 'CHEF_CLIENT')

        for key in config_keys:
            if not app.config[key]:
                raise Exception(key + " has not been set")

        return cls(*(app.config[x] for x in config_keys))

    def __init__(self, url, key, client):
        self.client = chef.api.ChefAPI(url, key, client)

    def _get(self, path):
        return self.client.api_request('GET', path)

    def get(self, *segments):
        return self._get('/' + '/'.join(segments))

    # Search API
    # GET /search

    def _search(self, index, query, keys=None, rows=1000, start=0):
        args = urllib.urlencode(dict(q=query, rows=rows, start=start))
        url = '/search/{0}?{1}'.format(index, args)
        method = 'POST' if keys is not None else 'GET'
        return self.client.api_request(method, url, data=keys)

    @staticmethod
    def _build_query(query, operator=' AND '):
        if isinstance(query, dict):
            return operator.join((k + ':' + v for k, v in query.items()))
        return query

    def search(self, index, query, rows=1000, start=0):
        return self._search(index, self._build_query(query), rows, start)

    # Partial Search API
    # POST /search

    @staticmethod
    def _build_partial_search(keys):
        """Create a partial_search from a list of attributes or a dict"""
        if isinstance(keys, (list, tuple)):
            keys = [key.split('.') for key in keys]
            keys = dict((key[0], key) for key in keys)
        return keys

    def partial_search(self, index, query, keys={}, rows=1000, start=0):
        """Returns data from a partial search (only returns defined keys)"""
        query = self._build_query(query)
        keys = self._build_partial_search(keys)

        # Sets a small number of very useful default attributes
        if index == 'node':
            keys.setdefault('name', ['name'])
            keys.setdefault('chef_environment', ['chef_environment'])

        # Returns data in this structure:
        # {rows: [{data: {...}, url: '...'}], start: 0, total: 1}
        results = self._search(index, query, keys, rows, start)

        # Return a list containing the returned data for each row
        return [row['data'] for row in results['rows']]

    # Higher-level search APIs

    def node(self, name, keys={}):
        """Returns a single node or raises an error"""
        nodes = self.partial_search('node', {'name': name}, keys)

        if len(nodes) != 1:
            raise chef.exceptions.ChefServerNotFoundError()

        return nodes[0]


class FlaskChefAPI(chef.ChefAPI):
    """Used to build a API client from a Flask app's configuration"""

    @classmethod
    def configure(cls, app):
        keys = ['CHEF_URL', 'CHEF_KEY', 'CHEF_CLIENT']
        args = [app.config[k] for k in keys]
        return cls(*args) if all(args) else chef.autoconfigure()


class PartialSearch(collections.Iterable):
    """Chef partial search implemenation, using PyChef

    A class similar to the existing Search class in PyChef, using Chef's
    partial search API - this only returns the requested keys and is much
    faster than a full search.

    Chef Search documentation:
        http://docs.opscode.com/essentials_search.html
        http://docs.opscode.com/api_chef_server_search_index.html
    """

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
