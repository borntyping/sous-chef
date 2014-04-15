# Uses fpm (https://github.com/jordansissel/fpm) to build a CentOS 6 RPM

vendor="Sam Clements <sam.clements@datasift.com>"
version=$(shell python setup.py --version)
release=1

sous-chef: dist/sous-chef-${version}-${release}.noarch.rpm

dist/sous-chef-${version}-${release}.noarch.rpm:
	@mkdir -p dist
	fpm -s python -t rpm \
	--package $@ --no-python-fix-name \
	--vendor ${vendor} \
	--epoch 1 --version ${version} --iteration ${release} \
	setup.py

# PyChef is not packaged for CentOS, so we also build an RPM for that

pychef_version=0.2.3
pychef_release=1

pychef: dist/python-pychef-${pychef_version}-${pychef_release}.noarch.rpm

dist/python-pychef-${pychef_version}-${pychef_release}.noarch.rpm:
	@mkdir -p dist
	fpm -s python -t rpm \
	--package $@ \
	--vendor ${vendor} \
	--epoch 1 --version ${pychef_version} --iteration ${pychef_release} \
	pychef

.PHONY: sous-chef pychef
