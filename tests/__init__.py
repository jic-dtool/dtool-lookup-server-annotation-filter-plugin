import os
import pathlib
import random
import string
import uuid
import tempfile
import shutil

import pytest

JWT_PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDV+7UTCb5JMX/GIY3g6kus84K5ko08nKbZcPgtRbTOkdNLFDcfotefNi+Y3bDEwMydXyc7uBmLkl9hyjBwTdCj6zAJ4VhLZ5wN0qg1cmg4Wkm6EUFgBHf7NY6V5M+v6XyZFinmzoe+J5llTH5xXLkieNMNtSDPUZWtRyhT9bwNSzYzBYZ13L1/yJJVUnb8mUmC2RG5ZqT8DZ+R/Y0Z35qACNmVqFTbSwFm3IoW2XcMXZawAKGoj0e9z6Eo6KZIRmVEFOfoeokz92zhS4b+j0+OJfmknpLYLHEyHswOnyFXFeNH1AHkGjDcAZwfr5ZMKpsy9XXlGiO2kFhK7RQ1ITvF olssont@n95996.nbi.ac.uk"  # NOQA

GRUMPY_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI5NjJjODEyNi1kZDJlLTQ1NDEtODQyOC0yZDYxYjEwZmU0M2YiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU1MzIyMzEzMywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU1MzIyMzEzMywiaWRlbnRpdHkiOiJncnVtcHkifQ.K1YYcUp2jfpBhVd7ggBJ_mpnQT_ZAGRjfgrReoz9no6zZ_5Hlgq2YLUNFtFfr2PrqsaO5fKWUfKrR8bjMijtlRlAEmyCJvalqXDWvriMf2QowyR6IjKxSNZcVCMkJXEk7cRlEM9f815YABc3RsG1F75n2dV5NSuvcQ4dQoItvNYpsuHZ3c-xYQuaQt7_Ch50Ez-H2fJatXQYdnHruyZOJQKPIssxU_yyeCnlOGklCmDn8mIolQEChrvW9HhpvgXsaAWEHjtNRK4T_ZH37Dq44fIB9ax6GGRZHDjWmjOicrGolfu73BuI8fOpLLpW5af6SKP-UhZA4AcW_TYG4PnOpQ"  # NOQA

SLEEPY_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhNzBhNmQ1ZS0xMTU4LTQ5YzAtOGM0OS02MmU1MzYzZWM3NDQiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU1MzIyMzIyNCwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU1MzIyMzIyNCwiaWRlbnRpdHkiOiJzbGVlcHkifQ.o15vGkZVsP_RaCIwXljFrkmFTef7ToPo_ssg7DPzRc33LhZh352gn6kY90JGMD1eyvrw69u6RwKW_5RkBmkDweCExiSDx7EuEofgadEegkM9qfbRfPGRpihobmQmwDADc6qspROUDi__gjrALLFZvg8cAteBVOBhKrItwHADym4RCHzDTyP0dd-k8PzvKUqBxryK5yutpc5Tkju3Bg33bFIyjJTr9kzZbjnzoYSjl1Nb7YtCO6ijsJasIPfLK8OOB2kza9NrAOAhWKqWtynzkyCCVckicfGZI5ywzNlsUqGcQwb7fNMUR-1JErM0wGViKOmotcQ08ut69KM5p8XZmg"  # NOQA

NOONE_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhMzUwY2MwZS1jMzAyLTQ1MGItYTE0NC01YTQzZjE3MDc4NDkiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU1MzI3NzA1MCwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU1MzI3NzA1MCwiaWRlbnRpdHkiOiJub29uZSJ9.VCRRsfLM5mwYz_viMVAJzfLf3_IF7MDTyzeWv3Ae_YYumu3UQVXUqWqJnvwyAY7KAqEIWkoFUET_bp-48WrvGaGr8q355IXiqspURpMMCLQ4G7Jwm3EnN6I61e_C6XpoyliZnd06qiVZR5VuaHxk41XclwRwgPCsEflj30SKWgVQOGbOYFfcSEdMKUvu8fyGbRwo47ynHvHrmxMAuURWjnN3g8gD-shBHCt1_4GVDSp1LSipSysDcn3-SdFa0PLGZqQ4Xj7QzM7AMmZ20J0uSHVA5U6RBzLU8d_neDdAg-Y2sjAC_G2P7jj0RdIU-QlDx2B25nyr4rOO9oSOI_q54Q"  # NOQA


def random_string(
    size=9,
    prefix="test_",
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
):
    return prefix + ''.join(random.choice(chars) for _ in range(size))


def randome_sqlite_uri(tmp_dir):
    fname = random_string() + ".sqlite"
    sqlite_fpath = pathlib.Path(os.path.join(tmp_dir, fname))
    raw_uri = sqlite_fpath.absolute().as_uri()

    sqlite_uri = "sqlite:/" + raw_uri[5:]
    if os.name == "nt":
        sqlite_uri = "sqlite" + raw_uri[4:]
    return sqlite_uri


def generate_dataset_info(base_uri, name, annotations):
    uri = "{}/{}".format(base_uri, uuid)
    new_uuid = str(uuid.uuid4())
    dataset_info = {
        "base_uri": base_uri,
        "type": "dataset",
        "uuid": new_uuid,
        "uri": uri,
        "name": name,
        "readme": {},
        "manifest": {
            "dtoolcore_version": "3.7.0",
            "hash_function": "md5sum_hexdigest",
            "items": {}
        },
        "creator_username": "dummy",
        "frozen_at": 1536238185.881941,
        "annotations": annotations,
        "tags": [],
    }
    return dataset_info


@pytest.fixture
def tmp_app(request):

    from dtool_lookup_server import create_app, mongo, sql_db
    from dtool_lookup_server.utils import (
        register_users,
        register_base_uri,
        register_dataset,
        update_permissions,
    )

    # Create temporary sqlite URI.
    d = tempfile.mkdtemp()
    sqlite_uri = randome_sqlite_uri(d)

    # Create temporary mongodb name.
    tmp_mongo_db_name = random_string()

    config = {
        "SECRET_KEY": "secret",
        "FLASK_ENV": "development",
        "SQLALCHEMY_DATABASE_URI": sqlite_uri,
        "MONGO_URI": "mongodb://localhost:27017/{}".format(tmp_mongo_db_name),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_ALGORITHM": "RS256",
        "JWT_PUBLIC_KEY": JWT_PUBLIC_KEY,
        "JWT_TOKEN_LOCATION": "headers",
        "JWT_HEADER_NAME": "Authorization",
        "JWT_HEADER_TYPE": "Bearer",
    }

    app = create_app(config)

    # Ensure the sql database has been put into the context.
    app.app_context().push()

    # Populate the database.
    sql_db.Model.metadata.create_all(sql_db.engine)

    # Register some users.
    username = "grumpy"
    register_users([
        dict(username=username),
        dict(username="sleepy"),
    ])

    # Register base URIs and set permissions.
    base_uri_1 = "s3://snow-white"
    base_uri_2 = "s3://mr-men"
    for base_uri in [base_uri_1, base_uri_2]:
        register_base_uri(base_uri)
        permissions = {
            "base_uri": base_uri,
            "users_with_search_permissions": [username],
            "users_with_register_permissions": [],
        }
        update_permissions(permissions)

    dataset_info = generate_dataset_info(
        base_uri_1,
        "blue-shirt",
        {"color": "blue"}
    )
    register_dataset(dataset_info)

    dataset_info = generate_dataset_info(
        base_uri_2,
        "red-wavy-shirt",
        {
            "color": "red",
            "pattern": "wavy",
            "complex_ignored": ["lists", "are", "ignored"]
        }
    )
    register_dataset(dataset_info)

    dataset_info = generate_dataset_info(
        base_uri_1,
        "stripy-shirt",
        {
            "pattern": "stripey",
            "color": ["purple", "gray"]  # Complex data type so ignored
        }
    )
    register_dataset(dataset_info)

    dataset_info = generate_dataset_info(
        base_uri_1,
        "complex-shirt",
        {
            "pattern": ["lies", "circles"],  # Complex data type so ignored
            "color": ["purple", "gray"]  # Complex data type so ignored
        }
    )
    register_dataset(dataset_info)  # Whole dataset ignored by plugin.

    @request.addfinalizer
    def teardown():
        mongo.cx.drop_database(tmp_mongo_db_name)
        sql_db.session.remove()
        shutil.rmtree(d)

    return app.test_client()
