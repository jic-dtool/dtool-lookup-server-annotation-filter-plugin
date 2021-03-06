"""Test utils.get_num_datasets_by_user utility function."""

import pytest

from . import tmp_app  # NOQA


def test_get_num_datasets_by_user_no_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_num_datasets_by_user
    )
    expected_key_info = 3
    actual_key_info = get_num_datasets_by_user(username="grumpy", filters={})  # NOQA
    assert expected_key_info == actual_key_info


def test_get_num_datasets_by_user_key_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_num_datasets_by_user
    )
    filters = {"annotation_keys": ["color"]}
    actual_key_info = get_num_datasets_by_user("grumpy", filters)  # NOQA
    expected_key_info = 2
    assert expected_key_info == actual_key_info


def test_get_num_datasets_by_user_base_uri_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_num_datasets_by_user
    )
    filters = {"base_uris": ["s3://mr-men"]}
    expected_key_info = 1
    actual_key_info = get_num_datasets_by_user("grumpy", filters)  # NOQA
    assert expected_key_info == actual_key_info


def test_get_num_datasets_by_user_annotations_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_num_datasets_by_user
    )
    filters = {
        "annotations": {"pattern": "stripey"}
    }
    expected_key_info = 1
    actual_key_info = get_num_datasets_by_user("grumpy", filters)  # NOQA
    assert expected_key_info == actual_key_info


def test_get_num_datasets_by_user_base_complex_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_num_datasets_by_user
    )
    filters = {
        "annotation_keys": ["pattern"],
        "annotations": {"pattern": "stripey"}
    }
    expected_key_info = 1
    actual_key_info = get_num_datasets_by_user("grumpy", filters)  # NOQA
    assert expected_key_info == actual_key_info

    filters = {
        "annotation_keys": ["color"],
        "annotations": {"pattern": "stripey"}
    }
    expected_key_info = 0
    actual_key_info = get_num_datasets_by_user("grumpy", filters)  # NOQA
    assert expected_key_info == actual_key_info


def test_authentication_error(tmp_app):  # NOQA
    from dtool_lookup_server import AuthenticationError
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_num_datasets_by_user
    )
    with pytest.raises(AuthenticationError):
        get_num_datasets_by_user("dont_exist", {})


def test_authorization(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_num_datasets_by_user
    )
    # The "sleepy" user has not got access to any datasets.
    actual_key_info = get_num_datasets_by_user(username="sleepy", filters={})  # NOQA
    assert actual_key_info == 0
