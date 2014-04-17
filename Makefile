# Uses fpm (https://github.com/jordansissel/fpm) to build RPMs for Sous-chef and
# it's direct dependencies (Flask's dependencies are provided by EPEL)

vendor="Sam Clements <sam.clements@datasift.com>"

define fpm
	@mkdir -p dist
	fpm -s python -t rpm --package $@ --vendor ${vendor} --epoch 1
endef


version=$(shell python setup.py --version)
release=1

sous-chef: dist/sous-chef-${version}-${release}.noarch.rpm

dist/sous-chef-${version}-${release}.noarch.rpm:
	${fpm} --version ${version} --iteration ${release} --no-python-fix-name setup.py

sous-chef.el6: dist/sous-chef-${version}-${release}el6.noarch.rpm

dist/sous-chef-${version}-${release}el6.noarch.rpm:
	${fpm} --version ${version} --iteration ${release}el6 \
	--no-python-fix-name \
	--no-python-dependencies \
	--depends 'python(abi) = 2.6' \
	--depends 'python-flask >= 2:0.10.1' \
	--depends 'python-pychef >= 0.2.3' \
	setup.py


flask_version=0.10.1
flask_release=1

flask: dist/python-flask-${flask_version}-${flask_release}.noarch.rpm

dist/python-flask-${flask_version}-${flask_release}.noarch.rpm:
	${fpm} --version ${flask_version} --iteration ${flask_release} flask

flask.el6: dist/python-flask-${flask_version}-${flask_release}el6.noarch.rpm

dist/python-flask-${flask_version}-${flask_release}el6.noarch.rpm:
	${fpm} \
	--epoch 2 --version ${flask_version} --iteration ${flask_release}el6 \
	--no-python-dependencies \
	--depends 'python(abi) = 2.6' \
	--depends 'python-itsdangerous >= 0.21' \
	--depends 'python-jinja2-26 >= 2.4' \
	--depends 'python-werkzeug >= 0.7' \
	flask


pychef_version=0.2.3
pychef_release=1

pychef: dist/python-pychef-${pychef_version}-${pychef_release}.noarch.rpm

dist/python-pychef-${pychef_version}-${pychef_release}.noarch.rpm:
	${fpm} --version ${pychef_version} --iteration ${pychef_release} pychef

all: sous-chef flask pychef
el6: sous-chef.el6 flask.el6 pychef

.PHONY: sous-chef sous-chef.el6 flask flask.el6 pychef all el6
