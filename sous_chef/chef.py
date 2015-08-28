"""A wrapper around PyChef to deal with configuration"""

from __future__ import absolute_import

import urllib  # urllib.parse for Python 3

import chef.api
import chef.exceptions


class Chef(object):
    @classmethod
    def from_flask_app(cls, app):
        config_keys = ('CHEF_URL', 'CHEF_KEY', 'CHEF_CLIENT')

        for key in config_keys:
            if key not in app.config:
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
    def normalise_keys(keys):
        """Create a partial_search from a list of attributes or a dict"""
        if isinstance(keys, (list, tuple)):
            keys = [key.split('.') for key in keys]
            keys = dict((key[0], key) for key in keys)
        return keys

    def partial_search(self, index, query, keys=None, rows=1000, start=0):
        """Returns data from a partial search (only returns defined keys)"""
        query = self._build_query(query)
        keys = self.normalise_keys(keys)

        # Returns data in this structure:
        # {rows: [{data: {...}, url: '...'}], start: 0, total: 1}
        results = self._search(index, query, keys, rows, start)

        # Return a list containing the returned data for each row
        return [row['data'] for row in results['rows']]
