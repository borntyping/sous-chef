"""sous-chef - A small webapp for viewing and searching Chef nodes"""

from __future__ import absolute_import

__version__ = '2.4.0'
__author__ = 'Sam Clements <sam.clements@datasift.com>'
__all__ = ['create_app', 'create_debug_app']


from sous_chef.app import create_app, create_debug_app
