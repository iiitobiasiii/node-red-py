import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='node-red-py',  # should match the package folder
    packages=['node-red-py'],  # should match the package folder
    version='0.0.1',  # important for updates
    license='GPLv3',  # should match your chosen license
    description='Testing installation of Package',
    long_description=long_description,  # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Tobias Busse',
    author_email='kontakt@tobiasbusse.de',
    url='https://github.com/',
    project_urls={  # Optional
        "Bug Tracker": "https://github.com/mike-huls/toolbox_public/issues"
    },
    install_requires=['requests'],  # list all packages that your package uses
    keywords=["pypi", "mikes_toolbox", "tutorial"],  # descriptive meta-data
    classifiers=[  # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    download_url="https://github.com/mike-huls/toolbox_public/archive/refs/tags/0.0.3.tar.gz",
)