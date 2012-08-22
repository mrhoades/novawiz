
A command-line client wrapping the openstack `nova` client.

Installation:
  `sudo pip install novawiz`

Usage:
  * `novawiz boot` - create an instance

  * `novawiz destroy` - destroy an instance

  * `novawiz image-build` - build a Glance image


Development:

  * to install to localhost: `python setup.py install`

  * to release a new verison to pypi:
    * bump version in setup.py
    * `python setup.py sdist upload`


