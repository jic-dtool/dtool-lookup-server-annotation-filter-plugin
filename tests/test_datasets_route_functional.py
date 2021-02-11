import json

from . import tmp_app  # NOQA
from . import GRUMPY_TOKEN, SLEEPY_TOKEN, NOONE_TOKEN

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

def test_datasets_route_all(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + GRUMPY_TOKEN)
    data = {}
    r = tmp_app.post(
        "/annotation_filter_plugin/datasets",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    assert(len(content) == 3)

    for ds_info in content:
        for expected_key in EXPECTED_DATASET_KEYS:
            assert expected_key in ds_info


def test_dataset_route_complex_with_multiple_keys_route(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + GRUMPY_TOKEN)
    data = {"annotation_keys": ["color", "pattern"]}
    r = tmp_app.post(
        "/annotation_filter_plugin/datasets",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    assert len(content) == 1
    assert content[0]["name"] == "red-wavy-shirt"


def test_datasets_route_with_sleepy_user(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + SLEEPY_TOKEN)
    data = {}
    r = tmp_app.post(
        "/annotation_filter_plugin/datasets",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 200
    content = json.loads(r.data.decode("utf-8"))
    assert content == []


def test_datasets_route_with_noone_user(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + NOONE_TOKEN)
    data = {}
    r = tmp_app.post(
        "/annotation_filter_plugin/datasets",
        headers=headers,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert r.status_code == 401
