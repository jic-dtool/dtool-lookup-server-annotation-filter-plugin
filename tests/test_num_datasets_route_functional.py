import json

from . import tmp_app  # NOQA
from . import GRUMPY_TOKEN, SLEEPY_TOKEN, NOONE_TOKEN


def test_num_datasets_route(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + GRUMPY_TOKEN)
    data = {}
    r = tmp_app.post(
        "/annotation_filter_plugin/num_datasets",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    expected_content = 3
    assert content == expected_content


def test_num_datasets_route_with_key_filter(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + GRUMPY_TOKEN)
    data = {"annotation_keys": ["color"]}
    r = tmp_app.post(
        "/annotation_filter_plugin/num_datasets",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    expected_content = 2
    assert content == expected_content


def test_num_datasets_route_with_annotation_filter(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + GRUMPY_TOKEN)
    data = {"annotations": {"pattern": "stripey"}}
    r = tmp_app.post(
        "/annotation_filter_plugin/num_datasets",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    expected_content = 1
    assert content == expected_content


def test_num_datasets_route_with_complex_filter(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + GRUMPY_TOKEN)

    data = {
        "annotation_keys": ["pattern"],
        "annotations": {"pattern": "stripey"}
    }
    r = tmp_app.post(
        "/annotation_filter_plugin/num_datasets",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    expected_content = 1
    assert content == expected_content


def test_num_datasets_route_with_sleepy_user(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + SLEEPY_TOKEN)
    data = {}
    r = tmp_app.post(
        "/annotation_filter_plugin/num_datasets",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    assert content == 0


def test_num_datasets_route_with_noone_user(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + NOONE_TOKEN)
    data = {}
    r = tmp_app.post(
        "/annotation_filter_plugin/num_datasets",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 401
