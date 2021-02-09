Specification for dtool lookup server filter plugin
===================================================


Introduction
------------

This dtool-lookup-server plugin adds the ability to get an overview of the
dataset a user has got access to based on how those datasets have been
annotated with key/value pairs.

The purpose of this REST API is to give users an overview of all the datasets
available to them and to allow them to drill down on those results by filtering
based upon keys and key/value pairs.


Routes
------

This plugin has four routes.

- GET /annotation_filter_plugin/keys
- GET /annotation_filter_plugin/annotation_values/<key>
- POST /annotation_filter_plugin/num_datasets
- POST /annotation_filter_plugin/datasets

The first gives access to all annotations keys that have are present on at
least one dataset with a basic value.

The second gives access to all values for a particular key.

The third gives the number of datasets given a particular annotation key/value filter.

The fourth gives the list of datasets given a particular annotation key/value filter.


Filter syntax
-------------

Below are examples of JSON queries that can be posted to the last two routes.

Get only datasets that have the key "species"::

    {
        "annotation_keys": ["species"]
    }

Get only datasets that have the "species" is set to "H. sapiens"::

    {
        "annotations": {"species": "H. sapiens"}
    }

Get only datasets that have both the keys "species" and "temperature"::

    {
        "annotation_keys": ["species", "temperature"]
    }

Get only datasets that have the "species" is set to "H. sapiens" and
"temperature" set to 25::

    {
        "annotations": {"species": "H. sapiens", "temperature": 25}
    }

Get only datasets that have the keys "species" and "temperature" and where the
"species" is set to "H. sapiens"::

    {
        "annotation_keys": ["species", "temperature"],
        "annotations": {"species": "H. sapiens"}
    }



Limitations
-----------

- This plugin only recognises annotations where the value is a basic type, such
  as a string, a number or a boolean value. In other words a dataset's
  annotations where the value is a  data structures such as lists and
  dictionaries will be ignored.
- Datasets that do not have any annotation with a basic type as a value will
  not be recognised up by this plugin.
