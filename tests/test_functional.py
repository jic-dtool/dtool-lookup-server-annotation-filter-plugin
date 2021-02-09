import json

from . import tmp_app  # NOQA
from . import GRUMPY_TOKEN, SLEEPY_TOKEN, NOONE_TOKEN


def test_keys_route_all(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + GRUMPY_TOKEN)
    data = {}
    r = tmp_app.post(
        "/annotation_filter_plugin/keys",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    expected_content = {"color": 2, "pattern": 2}
    assert content == expected_content


def test_keys_route_with_key_filter(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + GRUMPY_TOKEN)
    data = {"annotation_keys": ["color"]}
    r = tmp_app.post(
        "/annotation_filter_plugin/keys",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    expected_content = {"color": 2, "pattern": 1}
    assert content == expected_content


def test_keys_route_with_annotation_filter(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + GRUMPY_TOKEN)
    data = {"annotations": {"pattern": "stripey"}}
    r = tmp_app.post(
        "/annotation_filter_plugin/keys",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    expected_content = {"pattern": 1}
    assert content == expected_content


def test_keys_route_with_complex_filter(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + GRUMPY_TOKEN)

    data = {
        "annotation_keys": ["pattern"],
        "annotations": {"pattern": "stripey"}
    }
    r = tmp_app.post(
        "/annotation_filter_plugin/keys",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    expected_content = {"pattern": 1}
    assert content == expected_content

    data = {
        "annotation_keys": ["color"],
        "annotations": {"pattern": "stripey"}
    }
    r = tmp_app.post(
        "/annotation_filter_plugin/keys",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    expected_content = {}
    assert content == expected_content


def test_keys_route_with_sleepy_user(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + SLEEPY_TOKEN)
    data = {}
    r = tmp_app.post(
        "/annotation_filter_plugin/keys",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    assert content == {}


def test_keys_route_with_noone_user(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + NOONE_TOKEN)
    data = {}
    r = tmp_app.post(
        "/annotation_filter_plugin/keys",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 401
