# Copyright 2020, Guillermo Adrián Molina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import codecs
from setuptools import setup

# The following version is parsed by other parts of this package.
# Don't change the format of the line, or the variable name.
package_version = "1.0.0"

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='elasticsearch_forwarder',
    version=package_version,
    url='https://github.com/guillermomolina/elasticsearch_forwarder',
    author='Guillermo Adrián Molina',
    author_email='guillermomolina@hotmail.com',
    license='Apache License, Version 2.0',
    platforms='All',
    description='Elasticsearch Forwarder - forward messages to elasticsearch',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    py_modules=['elasticsearch_forwarder'],
    install_requires=[
        'distro',
        'elasticsearch',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'forwarder = forwarder:main',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: BSD :: NetBSD',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Operating System',
    ]
)