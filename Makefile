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


flask_version=0.10.1
flask_release=1

flask: dist/python-flask-${flask_version}-${flask_release}.noarch.rpm

dist/python-flask-${flask_version}-${flask_release}.noarch.rpm:
	${fpm} --version ${flask_version} --iteration ${flask_release} flask


pychef_version=0.2.3
pychef_release=1

pychef: dist/python-pychef-${pychef_version}-${pychef_release}.noarch.rpm

dist/python-pychef-${pychef_version}-${pychef_release}.noarch.rpm:
	${fpm} --version ${pychef_version} --iteration ${pychef_release} pychef

all: sous-chef flask pychef

.PHONY: sous-chef pychef all
