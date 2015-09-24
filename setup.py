import setuptools

setuptools.setup(
    name='sous-chef',
    version='2.6.0',
    url='https://github.com/datasift/sous-chef',

    author="Sam Clements",
    author_email="sam.clements@datasift.com",

    description="A web frontend for the Chef server index",
    long_description=open('README.rst').read(),
    license='MIT',

    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'flask>=0.10.0',
        'pychef>=0.2.3'
    ],

    extras_require={
        'debug': [
            'flask-debugtoolbar>=0.9.0'
        ],
        'deploy': [
            'gunicorn>=18.0'
        ]
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
)
