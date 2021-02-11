"""Test utils.get_num_datasets_by_user utility function."""

from . import tmp_app  # NOQA

EXPECTED_DATASET_KEYS = (
    "base_uri",
    "created_at",
    "creator_username",
    "frozen_at",
    "name",
    "type",
    "uri",
    "uuid",
    "annotations",
)


def test_get_datasets_by_user_no_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_datasets_by_user
    )
    content = get_datasets_by_user(username="grumpy", filters={})  # NOQA
    assert(len(content) == 3)

    for ds_info in content:
        for expected_key in EXPECTED_DATASET_KEYS:
            assert expected_key in ds_info


def test_get_dataset_by_user_annotation_key_filter_single(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_datasets_by_user
    )
    filters = {"annotation_keys": ["color"]}
    hits = get_datasets_by_user("grumpy", filters)  # NOQA
    assert len(hits) == 2
    expected_names = set(["blue-shirt", "red-wavy-shirt"])
    actual_names = set([i["name"] for i in hits])
    assert expected_names == actual_names


def test_get_datasets_by_user_annotation_key_filter_multiple(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_datasets_by_user
    )
    filters = {"annotation_keys": ["color", "pattern"]}
    hits = get_datasets_by_user("grumpy", filters)  # NOQA
    assert len(hits) == 1
    assert hits[0]["name"] == "red-wavy-shirt"


def test_get_datasets_by_user_annotation_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_datasets_by_user
    )
    filters = {"annotation_keys": ["color"], "annotations": {"pattern": "wavy"}}  # NOQA
    hits = get_datasets_by_user("grumpy", filters)  # NOQA
    assert len(hits) == 1
    assert hits[0]["name"] == "red-wavy-shirt"


def test_get_datasets_by_user_complex_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_datasets_by_user
    )
    filters = {"annotations": {"color": "red"}}
    hits = get_datasets_by_user("grumpy", filters)  # NOQA
    assert len(hits) == 1
    assert hits[0]["name"] == "red-wavy-shirt"


def test_get_datasets_by_user_base_uri_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_datasets_by_user
    )
    filters = {"base_uris": ["s3://mr-men"], "annotation_keys": ["pattern"]}
    hits = get_datasets_by_user("grumpy", filters)  # NOQA
    assert len(hits) == 1
    assert hits[0]["name"] == "red-wavy-shirt"
