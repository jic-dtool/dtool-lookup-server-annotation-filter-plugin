dtool-lookup-server-annotation-filter-plugin
============================================

.. image:: https://badge.fury.io/py/dtool-lookup-server-annotation-filter-plugin.svg
   :target: http://badge.fury.io/py/dtool-lookup-server-annotation-filter-plugin
   :alt: PyPi package

.. image:: https://travis-ci.org/jic-dtool/dtool-lookup-server-annotation-filter-plugin.svg?branch=master
   :target: https://travis-ci.org/jic-dtool/dtool-lookup-server-annotation-filter-plugin
   :alt: Travis CI build status (Linux)

.. image:: https://codecov.io/github/jic-dtool/dtool-lookup-server-annotation-filter-plugin/coverage.svg?branch=master
   :target: https://codecov.io/github/jic-dtool/dtool-lookup-server-annotation-filter-plugin?branch=master
   :alt: Code Coverage

- GitHub: https://github.com/jic-dtool/dtool-lookup-server-annotation-filter-plugin
- PyPI: https://pypi.python.org/pypi/dtool-lookup-server-annotation-filter-plugin
- Free software: MIT License


Introduction
------------

This `dtool-lookup-server <https://github.com/jic-dtool/dtool-lookup-server>`_
plugin adds the ability to get an overview of the dataset a user has got access
to based on how those datasets have been annotated with key/value pairs.

The purpose of this API is to give users an overview of all the datasets
available to them and to allow them to drill down on those results by filtering
based upon keys and key/value pairs.

This API could be used to build a webapp that allows users to get an
"eagle-eye" view of their data.


Installation
------------

This plugin depends on having installed and configured a  `dtool-lookup-server
<https://github.com/jic-dtool/dtool-lookup-server>`_. This plugin can then
be installed by running the commands below.

::

    git clone https://github.com/jic-dtool/dtool-lookup-server-annotation-filter-plugin.git
    cd dtool-lookup-server-annotation-filter-plugin
    python setup.py install

See `dtool-lookup-server <https://github.com/jic-dtool/dtool-lookup-server>`_
for more information about the setup of the base system.


Routes
------

This plugin has five routes.

- POST /annotation_filter_plugin/annotation_keys
- POST /annotation_filter_plugin/annotation_values
- POST /annotation_filter_plugin/num_datasets
- POST /annotation_filter_plugin/datasets
- GET /annotation_filter_plugin/version

The first gives access to all annotations keys that have are present on at
least one dataset with a basic value. The keys will only be extracted from
datasets that pass any annotation filter in the post request. The response from
this route includes information about the number of datasets associated with
each key.

The second gives access to all values for the keys specified in the post
request.  The values will only be extracted from the datasets that pass the
annotation filter in the post request. The response form this route includes
information about the number of datasets associated with each key/value pair.

The third gives the number of datasets given a particular annotation filter.

The fourth gives the list of datasets given a particular annotation filter.

The fifth returns the version of the plugin.


Filter syntax
-------------

Below are examples of JSON queries that can be posted to the  routes.

No filters, i.e. get all (this only really makes sense for the
/annotation_filter_plugin/annotation_keys route).

::

    {}

Get only datasets that have the key "color"::

    {
        "annotation_keys": ["color"]
    }

Get only datasets that have the "color" is set to "red"::

    {
        "annotations": {"color": "red"}
    }

Get only datasets that have both the keys "color" and "pattern"::

    {
        "annotation_keys": ["color", "pattern"]
    }

Get only datasets that have the "color" is set to "red" and
"pattern" set to "stripey"::

    {
        "annotations": {"color": "red", "pattern": "stripey"}
    }

Get only datasets that have the keys "color" and "pattern" and where the
"color" is set to "red"::

    {
        "annotation_keys": ["color", "pattern"],
        "annotations": {"color": "red"}
    }



Limitations
-----------

- This plugin only recognises annotations where the value is a basic type, such
  as a string, a number or a boolean value. In other words a dataset's
  annotations where the value is a  data structures such as lists and
  dictionaries will be ignored.
- Datasets that do not have any annotation with a basic type as a value will
  not be recognised up by this plugin.


Usage
-----

Preparation
~~~~~~~~~~~

The dtool lookup server makes use of the Authorization header to pass through the
JSON web token for authorization. Below we create environment variables for the
token and the header used in the ``curl`` commands::

    $ TOKEN=$(flask user token olssont)
    $ HEADER="Authorization: Bearer $TOKEN"


Find keys available for filtering and the number of datasets associated with them
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The command below finds all annotations keys available for further filtering::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{}'  \
        http://localhost:5000/annotation_filter_plugin/annotation_keys

The response below means that the annotation key "color" has 120 datasets
associated with it and the annotation key "pattern" has 50 datasets associated
with it.

::

    {"color": 120, "pattern": 50, "size": 10}

Suppose that one chooses to filter further based on the "pattern" annotation key.
Using the command below one could find the annotation keys that are still relevant
given that each dataset has to have the annotation key "pattern".

::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{"annotation_keys": ["pattern"]}'  \
        http://localhost:5000/annotation_filter_plugin/annotation_keys

The response below shows that no datasets that remain have the key "size" and
45 of the datasets with the key "pattern" also have the key "color".

::

    {"color": 45, "pattern": 50}

It is possible to filter based on an annotation key/value pair. For example, to
limit the datasets to the case where the "pattern" is "stripey" one could use
the command below.

::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{"annotations": {"pattern": "stripey"}}'  \
        http://localhost:5000/annotation_filter_plugin/annotation_keys

The response below shows that this is more specific and that there are fewer
results.

::

    {"color": 5, "pattern": 10}

It is possible to make more complex queries. The command below also requires
that the datasets have the key "color".

::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{"annotation_keys": ["color"], "annotations": {"pattern": "stripey"}}'  \
        http://localhost:5000/annotation_filter_plugin/annotation_keys

In the response below there are now fewer datasets with the "pattern" key. That
is because some of the datasets that were picked up previously did not have the
"color" key.

::

    {"color": 5, "pattern": 3}

It is also possible to filter using base URIs. The command below limits the
keys to those from the base URIs "s3://snow-white" and "s3://mr-men"::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{"base_uris": ["s3://snow-white", "s3://mr-men"]}'  \
        http://localhost:5000/annotation_filter_plugin/annotation_keys

The response below shows that there are fewer hits than when all base URIs
are included.

::

    {"color": 77, "pattern": 35, "size": 4}


Find annotations available for filtering and the number of datasets associated with them
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pattern for finding annotation key/value pairs and the number of datasets assocated
with them is similar to that of finding the keys (above).

The command below can be used to find all the values associated with the "color" key and
the number of datasets that has been annotated with each particular value.

::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{"annotation_keys": ["color"]}'  \
        http://localhost:5000/annotation_filter_plugin/annotation_values

The response below shows that there are five colors available and that most datasets
have the color "red".

::

    {
        "color": {
            "red": 50,
            "pink": 30,
            "blue": 20,
            "green": 15,
            "yellow": 5
        }
    }

To get data for more keys they need to be included in the filter. The command below
returns the datasets that have annotations for both "color" and "pattern".

::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{"annotation_keys": ["color", "pattern"]}'  \
        http://localhost:5000/annotation_filter_plugin/annotation_values

The response contains less colors because some of the datasets annotated with color
did not have a pattern annotation.

::

    {
        "color": {
            "red": 15,
            "pink": 10,
            "blue": 10,
            "green": 10
        }
        "pattern": {
            "stripey": 40,
            "wavy": 10
    }

It is possible to make more specific queries. The command below also requires
that the datasets have the stripey pattern.

::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{"annotation_keys": ["color"], "annotations": {"pattern": "stripey"}}'  \
        http://localhost:5000/annotation_filter_plugin/annotation_keys

The response below shows that fewer datasets have been used to collect the
annotation information.

::

    {
        "color": {
            "red": 15,
            "pink": 10,
            "blue": 10,
            "green": 5
        }
        "pattern": {
            "stripey": 40,
    }

It is also possible to filter using base URIs. The command below limits the
keys to those from the base URIs "s3://snow-white" and "s3://mr-men"::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{"annotation_keys": ["color"], "base_uris": ["s3://snow-white", "s3://mr-men"]}'  \
        http://localhost:5000/annotation_filter_plugin/annotation_keys

The response below shows that there are fewer hits than when all base URIs
are included.

::

    {
        "color": {
            "red": 50,
            "pink": 20,
            "blue": 7,
        }
    }


Listing the number of datasets available for a particular filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The number of datasets selected, using a particular filter, can be determined using the
``/annotation_filter_plugin/num_datasets`` route. The command below selects all datasets
with at least one basic value (see the section below on limitations for an explanation
of what a basic value is). 

::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{}'  \
        http://localhost:5000/annotation_filter_plugin/num_datasets

The response below shows that there are 145 such datasets.

::

        145

The command below uses a filter to select only datasets that have the key/value
pair "pattern"/"stripey".

::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{"annotations": {"pattern": "stripey"}}'  \
        http://localhost:5000/annotation_filter_plugin/num_datasets

The response shows that there are 10 such datasets.

::

        10

Retrieving information about datasets selected by a particular filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to get information about the datasets selected by a particular
filter using the ``/annotation_filter_plugin/datasets`` route. The command
below uses a filter to select only datasets that have the key/value pair
"pattern"/"stripey".

::

    $ curl -H "$HEADER" -H "Content-Type: application/json"  \
        -X POST -d '{"annotations": {"pattern": "stripey"}}'  \
        http://localhost:5000/annotation_filter_plugin/datasets

Below is a truncated version of the response.

::

    [
      {
        "annotations": {
          "pattern": "stripey
        },
        "base_uri": "s3://dtool-demo",
        "created_at": "1530803916.74",
        "creator_username": "olssont",
        "dtoolcore_version": "3.3.0",
        "frozen_at": "1536749825.85",
        "name": "hypocotyl3",
        "type": "dataset",
        "uri": "s3://dtool-demo/ba92a5fa-d3b4-4f10-bcb9-947f62e652db",
        "uuid": "ba92a5fa-d3b4-4f10-bcb9-947f62e652db"
      }
      ...
    ]
