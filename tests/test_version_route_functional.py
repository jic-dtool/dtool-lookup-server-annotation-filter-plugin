import json

from . import tmp_app  # NOQA
from . import GRUMPY_TOKEN, NOONE_TOKEN


def test_version_route(tmp_app):  # NOQA

    from dtool_lookup_server_annotation_filter_plugin import __version__
    headers = dict(Authorization="Bearer " + GRUMPY_TOKEN)
    r = tmp_app.get(
        "/annotation_filter_plugin/version",
        headers=headers,
    )
    assert r.status_code == 200
    response = json.loads(r.data.decode("utf-8"))
    assert response == __version__


def test_num_datasets_route_with_noone_user(tmp_app):  # NOQA
    headers = dict(Authorization="Bearer " + NOONE_TOKEN)
    r = tmp_app.get(
        "/annotation_filter_plugin/version",
        headers=headers,
        content_type="application/json"
    )
    assert r.status_code == 401
