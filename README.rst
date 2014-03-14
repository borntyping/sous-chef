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

The optional environment variable ``SOUS_CHEF_SETTINGS`` can be pointed at a
Flask configuration file (`docs`_).

The app can be run in debug mode by using the `create_debug_app` function:

::

	gunicorn 'sous_chef:create_debug_app()'

The ``flask-debugtoolbar`` package is availible, the DebugToolbar extension will
be used.

.. _docs: http://flask.pocoo.org/docs/config/#configuring-from-files

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

Targets Python 2.7, 3.3 and above.

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
