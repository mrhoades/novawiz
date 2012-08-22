
A command-line client wrapping the openstack `nova` client.

Installation:
  `sudo pip install novawiz`

Usage:
  * `novawiz boot` - create an instance

  * `novawiz destroy` - destroy an instance

  * `novawiz image-build` - build a Glance image


Development:

  * to install to your machine
    `python setup.py install`

  * to release a new verison to pypi
    edit version in setup.py
    `python setup.py sdist upload`


