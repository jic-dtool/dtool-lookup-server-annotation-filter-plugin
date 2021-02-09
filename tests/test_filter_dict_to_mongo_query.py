"""Test utils.filter_dict_to_mongo_query utility function."""


def test_one_uri():
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        filter_dict_to_mongo_query
    )
    expected = {"base_uri": "a"}
    actual = filter_dict_to_mongo_query({"base_uris": ["a"]})
    assert actual == expected


def test_multiple_uris():
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        filter_dict_to_mongo_query
    )
    expected = {"base_uri": {"$in": ["a", "b"]}}
    actual = filter_dict_to_mongo_query({"base_uris": ["a", "b"]})
    assert actual == expected
