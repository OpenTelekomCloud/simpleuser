Usermanagement
==============

This script is a poor man's user management. If you use its write
mode, it will create users described in a JSON file and assign it to
projects of a domain, limiting the listed user to log into and work
only in that domain.

If you use the script in its read mode, it extracts all user and
project data from a given domain and prints a config file that can be
consumed by the write mode again.

The OpenStack user and project model allows for much more options and
modes, but this script restricts explicitly those options. If you plan
to do more fine grained user, project, and policy managment, see
XXX wherever XXX.

Architecture
------------

Installation
------------

How to use
----------

Examples
--------

Author
------

Copyright (c) 2019 by Nils Magnus (nils.magnus@t-systems.com) for Open
Telekom Cloud, T-Systems International GmbH.

License
-------

This software is licensed under the Apache 2 license.
