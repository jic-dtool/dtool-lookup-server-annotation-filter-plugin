import json

from . import tmp_app  # NOQA
from . import GRUMPY_TOKEN


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
