"""Test utils.annotation_value_info_by_user utility function."""

import pytest

from . import tmp_app  # NOQA


def test_get_annotation_values_by_user_no_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_annotation_value_info_by_user
    )
    expected_key_info = {}
    actual_key_info = get_annotation_value_info_by_user(username="grumpy", filters={})  # NOQA
    assert expected_key_info == actual_key_info


def test_get_annotation_values_by_user_annotation_key_filter_single(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_annotation_value_info_by_user
    )
    filters = {"annotation_keys": ["color"]}
    actual_key_info = get_annotation_value_info_by_user("grumpy", filters)  # NOQA
    expected_key_info = {"color": {"blue": 1, "red": 1}}
    assert expected_key_info == actual_key_info


def test_get_annotation_values_by_user_annotation_key_filter_multiple(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_annotation_value_info_by_user
    )
    filters = {"annotation_keys": ["color", "pattern"]}
    actual_key_info = get_annotation_value_info_by_user("grumpy", filters)  # NOQA
    expected_key_info = {"color": {"red": 1}, "pattern": {"wavy": 1}}
    assert expected_key_info == actual_key_info


def test_get_annotation_values_by_user_annotation_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_annotation_value_info_by_user
    )
    filters = {"annotation_keys": ["color"], "annotations": {"pattern": "wavy"}}
    actual_key_info = get_annotation_value_info_by_user("grumpy", filters)  # NOQA
    expected_key_info = {"color": {"red": 1}, "pattern": {"wavy": 1}}
    assert expected_key_info == actual_key_info


def test_get_annotation_values_by_user_complex_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_annotation_value_info_by_user
    )
    filters = {"annotations": {"color": "red"}}
    actual_key_info = get_annotation_value_info_by_user("grumpy", filters)  # NOQA
    expected_key_info = {"color": {"red": 1}}
    assert expected_key_info == actual_key_info


def test_get_annotation_values_by_user_base_uri_filter(tmp_app):  # NOQA
    from dtool_lookup_server_annotation_filter_plugin.utils import (
        get_annotation_value_info_by_user
    )
    filters = {"base_uris": ["s3://snow-white"], "annotatoin_keys": ["pattern"]}
    expected_key_info = {"pattern": {"wavy": 1}}
    actual_key_info = get_annotation_value_info_by_user("grumpy", filters)  # NOQA
    assert expected_key_info == actual_key_info
