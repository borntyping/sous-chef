# Uses fpm (https://github.com/jordansissel/fpm) to build RPMs for Sous-chef and
# it's direct dependencies (Flask's dependencies are provided by EPEL)

vendor="Sam Clements <sam.clements@datasift.com>"

define fpm
	@mkdir -p dist
	fpm -s python -t rpm --package $@ --vendor ${vendor} --epoch 0
endef


default:
	@echo "Usage:"
	@echo "  make all - build RPMs for Sous-chef and dependencies"
	@echo "  make {sous-chef,flask,pychef} - Build single specific RPMs"
	@echo "RPM's are targeted at CentOS 6"

all: sous-chef flask jinja2 pychef


version=$(shell python setup.py --version)
release=5

sous-chef: dist/sous-chef-${version}-${release}.el6.noarch.rpm

dist/sous-chef-${version}-${release}.el6.noarch.rpm:
	${fpm} --version ${version} --iteration ${release}.el6 \
	--no-python-fix-name setup.py


flask_version=0.10.1
flask_release=4

flask: dist/python-flask-${flask_version}-${flask_release}.el6.noarch.rpm

dist/python-flask-${flask_version}-${flask_release}.el6.noarch.rpm:
	${fpm} --epoch 2 --version ${flask_version} --iteration ${flask_release}.el6 flask


jinja2_version=2.7.2
jinja2_release=1

jinja2: dist/python-jinja2-${jinja2_version}-${jinja2_release}.el6.noarch.rpm

dist/python-jinja2-${jinja2_version}-${jinja2_release}.el6.noarch.rpm:
	${fpm} --epoch 2 --version ${jinja2_version} --iteration ${jinja2_release}.el6 jinja2


pychef_version=0.2.3
pychef_release=4

pychef: dist/python-pychef-${pychef_version}-${pychef_release}.el6.noarch.rpm

dist/python-pychef-${pychef_version}-${pychef_release}.el6.noarch.rpm:
	${fpm} --version ${pychef_version} --iteration ${pychef_release}.el6 \
	--depends 'openssl-devel' pychef


.PHONY: default all sous-chef flask jinja2 pychef
