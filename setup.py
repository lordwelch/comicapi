from setuptools import setup
setup(
        name = 'comicapi',
        version = '2.1.1',
        description = 'Comic archive (cbr/cbz/cbt) and metadata utilities. Extracted from the comictagger project.',
        author = 'Iris W',
        packages = ['comicapi'],
        install_requires = ['natsort>=3.5.2'],
        extras_require = {
            'CBR': ['rarfile==2.7']
        },
        python_requires = '>=2.7.0',
        url = 'https://github.com/OzzieIsaacs/comicapi',
        classifiers = ['License :: OSI Approved :: Apache Software License 2.0 (Apache-2.0)']
)
