CHANGELOG
=========

This project uses `semantic versioning <http://semver.org/>`_.
This change log uses principles from `keep a changelog <http://keepachangelog.com/>`_.

[Unreleased]
------------


Added
^^^^^


Changed
^^^^^^^


Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^


Security
^^^^^^^^


[0.2.1] - 2022-05-20
--------------------

Fixed
^^^^^

- Make code compatible with version 4 of the jwt-extended API


[0.2.0] - 2021-02-13
--------------------

Added
^^^^^

- Made the package python 2 compatible

Fixed
^^^^^

- Fixed defect where legacy datasets without annotations caused a KeyError to be raised;
  https://github.com/jic-dtool/dtool-lookup-server-annotation-filter-plugin/issues/1


[0.1.1] - 2021-02-12
--------------------

Fixed
^^^^^

- Added long description to setup.py


[0.1.0] - 2021-02-12
--------------------

Initial release with five routes.

- POST /annotation_filter_plugin/annotation_keys
- POST /annotation_filter_plugin/annotation_values
- POST /annotation_filter_plugin/num_datasets
- POST /annotation_filter_plugin/datasets
- GET /annotation_filter_plugin/version
