import setuptools

setuptools.setup(
    name="sous-chef",
    version="0.2.0",
    url="https://github.com/borntyping/sous-chef",

    author="Sam Clements",
    author_email="sam.clements@datasift.com",

    description="A small webapp for viewing and searching Chef nodes",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'flask==0.10.1',
        'pychef==0.2.3'
    ],

    entry_points={
        'console_scripts': [
            'sous-chef = sous_chef:main'
        ]
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
