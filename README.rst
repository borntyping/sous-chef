Sous-chef
=========

.. image:: https://pypip.in/v/sous-chef/badge.png
    :target: https://pypi.python.org/pypi/sous-chef
    :alt: Latest PyPI version

A small webapp for viewing and searching Chef nodes.

Usage
-----

::

	gunicorn 'sous_chef:create_app()'

Sous-chef will read it's configuration from a ``config.py`` file in a `Flask
instance folder`_ - for a global install this is
``/usr/var/sous_chef-instance``, and for a virtualenv install this is
``/``$VIRTUALENV/var/sous_chef-instance``.

The Flask settings ``CHEF_URL``, ``CHEF_KEY`` and ``CHEF_CLIENT`` are used to
create a Chef API client, using PyChef's ``autoconfigure`` as a fallback.
``DEFAULT_CHEF_ENVIRONMENT`` sets the Chef environment to show nodes from by
default. See ``sous_chef/defaults.py`` for more information on the configuration
options.

The app can be run in debug mode by using the ``create_debug_app`` function::

	gunicorn 'sous_chef:create_debug_app()'

The ``flask-debugtoolbar`` package is availible, the DebugToolbar extension will
be used.

.. _Flask instance folder: http://flask.pocoo.org/docs/config/#instance-folders

Installation
------------

::

	pip install sous-chef gunicorn

Requirements
^^^^^^^^^^^^

Requires `Flask`_ and `PyChef`_. `Gunicorn`_ is the simplest method of
deployment, but is not a requirement (allowing alternate WSGI servers to be
used). Optionally uses `Flask Debug Toolbar`_ using the debug application.

.. _Flask: http://flask.pocoo.org/
.. _PyChef: https://github.com/coderanger/pychef
.. _Gunicorn: http://gunicorn.org/
.. _Flask Debug Toolbar: https://pypi.python.org/pypi/Flask-DebugToolbar

Compatibility
^^^^^^^^^^^^^

Targets Python 2.6 and 2.7.

PyChef is currently Python 2 only, but if or when it is availible for Python 3
Sous-chef should have no problems.

Licence
-------

The MIT License (MIT)

Copyright (c) 2014 DataSift <opensource@datasift.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Authors
-------

``sous-chef`` was written by `Sam Clements <sam.clements@datasift.com>`_ at
`DataSift <https://datasift.com>`_.

.. image:: https://gravatar.com/avatar/8dd5661684a7385fe723b7e7588e91ee?s=40
.. image:: https://gravatar.com/avatar/a3a6d949b43b6b880ffb3e277a65f49d?s=40
