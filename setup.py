#from __future__ import print_function
import ast
import os
import sys
import codecs
import subprocess
from fnmatch import fnmatchcase
from distutils.util import convert_path
from setuptools import setup, find_packages


def find_version(*parts):
    try:
        version_py = os.path.join(os.path.dirname(__file__), 'django_extended/version.py')
        version_git = subprocess.check_output(["git", "tag"]).rstrip().splitlines()[-1]
        version_msg = "# Do not edit this file, pipeline versioning is governed by git tags" + os.linesep + "# following PEP 386"
        open(version_py, 'wb').write(version_msg + os.linesep + '__version__ = "%s"' % version_git)

    except:
        # NOT RAN LOCALY
        pass

    from django_extended.version import __version__
    return "{ver}".format(ver=__version__)

def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()



# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ('*.py', '*.pyc', '*$py.class', '*~', '.*', '*.bak')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build',
                                './dist', 'EGG-INFO', '*.egg-info')

setup(
    name='django-extended',
    version=find_version(),
    description='Django extended stuffs',
    long_description=read('README.rst'),
    author='Autrusseau Damien',
    author_email='autrusseau.damien@gmail.com',
    url='http://github.com/dalou/django-extended',
    packages=find_packages(exclude=('tests*',)),
    zip_safe=False,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    # test_suite='runtests.runtests',
    install_requires=[
        'django>=1.8.4,<=1.9',
        "jsonfield==1.0.3",
        "babel==1.3",
        "premailer==2.9.6"
    ],
)
