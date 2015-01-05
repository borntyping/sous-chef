Sous-chef
=========

.. image:: http://img.shields.io/pypi/v/sous-chef.svg?style=flat-square
    :target: https://pypi.python.org/pypi/sous-chef
    :alt: Sous-chef on PyPI

.. image:: http://img.shields.io/pypi/l/sous-chef.svg?style=flat-square
    :target: https://pypi.python.org/pypi/sous-chef
    :alt: Sous-chef on PyPI

.. image:: http://img.shields.io/travis/borntyping/sous-chef/master.svg?style=flat-square
    :target: https://travis-ci.org/borntyping/sous-chef
    :alt: Travis-CI build status for Sous-chef

.. image:: https://img.shields.io/github/issues/borntyping/sous-chef.svg?style=flat
    :target: https://github.com/borntyping/sous-chef/issues
    :alt: GitHub issues for Sous-chef

|

A web frontend for the Chef server index, displaying nodes, roles and
environments, as well as data collected by Ohai plugins (in particular,
installed package versions).



Installation
------------

Install Sous-chef and Gunicorn with::

	pip install 'sous-chef[deploy]'

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

Targets Python 2.6 and 2.7, due to the dependency on `PyChef`_.



Usage
-----

Run Sous-chef using `Gunicorn`_::

	gunicorn 'sous_chef:create_app()'

Configuration
^^^^^^^^^^^^^

Sous-chef will read it's configuration from one of two places, depending on how
it was installed::

	# Global install
	/usr/var/sous_chef-instance/config.py

	# Virtualenv install
	$VIRTUALENV/var/sous_chef-instance/config.py

An example configuration file might look like this::

	# The URL of the Chef server
	CHEF_URL = 'http://chef.example.com'

	# The client name and key to use
	CHEF_CLIENT = 'sous'
	CHEF_KEY = '/usr/var/sous_chef-instance/sous.pem'

If these are not set, PyChef's ``autoconfigure`` function is used as a fallback,
and will try and load it's configuration from ``~/.chef/knife.rb`` or
``/etc/chef/client.rb``.

Package versions
^^^^^^^^^^^^^^^^

Sous-chef will display package metadata from nodes if available. It expects this
data to be in the following format::

	"packages": {
		"<package_type>": {
			"<package_name>": {
				"version": "<package_version"
			},
			...
		},
		...
	}

For example, an RPM Ohai plugin could set the following node attributes::

	"packages": {
		"rpm": {
			"package-one": {
				"version": "0.1.0",
			},
			"package-two": {
				"version": "2.0.1",
			}
		}
	}

Debug mode
^^^^^^^^^^

The application can be run in debug mode by using the ``create_debug_app``
function::

	gunicorn 'sous_chef:create_debug_app()'

If the ``flask-debugtoolbar`` package is available, the `DebugToolbar`_
extension will be loaded and can be used to show debug information in a browser.

.. _DebugToolbar: http://flask-debugtoolbar.readthedocs.org/en/latest/



Contributing
------------

Contributions are very welcome - issues and feature requests should use the
`github issue tracker`_, and pull requests should be made against the develop
branch.

Issues are assigned tags of *easy*, *medium* and *hard*, giving some indication
of how easy a feature request should be to implement or how hard a bug will be
to fix. Fixes or implementations for any unassigned issues are welcome.

Bear in mind that new functionality should be useful for all users of the
application - features that can only be used with internal components or that
require significant infrastructure beyond a Chef server are unlikely to be
approved (though are still open to discussion).

.. _github issue tracker: https://github.com/datasift/sous-chef/issues

Code Style and Design
^^^^^^^^^^^^^^^^^^^^^

Python code should use the style from `PEP8`_, and preferably pass all `flake8`_
tests. Version numbers should use the `Semantic Versioning`_ specification, and
are set in both ``setup.py`` and ``sous_chef/__init__.py``.

As much functionality as possible should work 'out of the box' and run without
needing explicit configuration - features that *do* require configuration to use
should either fall back to an alternative or be off by default.

Optional integrations (such as the existing Flask DebugToolbar integration)
should define requirements in ``extras_require`` instead of ``install_requires``
and ensure that they do not crash if the requirement is not present.

.. _PEP8: http://legacy.python.org/dev/peps/pep-0008/
.. _flake8: https://flake8.readthedocs.org/en/2.0/
.. _Semantic Versioning: http://semver.org/spec/v2.0.0.html



Licence
-------

Sous-Chef is licensed under the MIT License.

This project includes copies of `Bootstrap`_ and `jQuery`_, both of which are
also licensed under the MIT Licence.

.. _Bootstrap: http://getbootstrap.com/
.. _jQuery: http://jquery.com/

Copyright (c) 2014 DataSift <opensource@datasift.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



Authors
-------

``sous-chef`` was written by `Sam Clements <sam.clements@datasift.com>`_ at
`DataSift <https://datasift.com>`_.

.. image:: https://gravatar.com/avatar/8dd5661684a7385fe723b7e7588e91ee?s=40
.. image:: https://gravatar.com/avatar/a3a6d949b43b6b880ffb3e277a65f49d?s=40
