dtool-lookup-server-annotation-filter-plugin
============================================


Installation
------------

::

    git clone https://github.com/jic-dtool/dtool-lookup-server-annotation-filter-plugin.git
    cd dtool-lookup-server-annotation-filter-plugin
    python setup.py install


Usage
-----

See `dtool-lookup-server <https://github.com/jic-dtool/dtool-lookup-server>`_ for more
information about the setup of the base system.


Preparation
~~~~~~~~~~~

The dtool lookup server makes use of the Authrized header to pass through the
JSON web token for authrization. Below we create environment variables for the
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
        -X POST -d '{"annotation_keys": "pattern"}'  \
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
