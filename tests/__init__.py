import os
import random
import string
import uuid
import tempfile
import shutil

import pytest

#

JWT_PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8LrEp0Q6l1WPsY32uOPqEjaisQScnzO/XvlhQTzj5w+hFObjiNgIaHRceYh3hZZwsRsHIkCxOY0JgUPeFP9IVXso0VptIjCPRF5yrV/+dF1rtl4eyYj/XOBvSDzbQQwqdjhHffw0TXW0f/yjGGJCYM+tw/9dmj9VilAMNTx1H76uPKUo4M3vLBQLo2tj7z1jlh4Jlw5hKBRcWQWbpWP95p71Db6gSpqReDYbx57BW19APMVketUYsXfXTztM/HWz35J9HDya3ID0Dl+pE22Wo8SZo2+ULKu/4OYVcD8DjF15WwXrcuFDypX132j+LUWOVWxCs5hdMybSDwF3ZhVBH ec2-user@ip-172-31-41-191.eu-west-1.compute.internal"  # NOQA

GRUMPY_TOKEN = "eyj0exaioijkv1qilcjhbgcioijsuzi1nij9.eyjmcmvzaci6zmfsc2usimlhdci6mtyymtewmty0nywianrpijoiywfmmtc3ntqtnzc4mi00odazlthlzditodzhymi0zdvhythliiwidhlwzsi6imfjy2vzcyisinn1yii6imdydw1wesisim5izii6mtyymtewmty0n30.tvytnoflegjpm1amdmqxe-2caa7je3uhq5dequtuugyumhyt7phsam8l0ahgqjlczb2x98gs9qeq5rxwxp5y8oteqzk26qbunw3jpg46e1pheesurqosclgyyika6ahtztb5aa5vxk2lgfb13jrqz03gjpudpqj7q1lbu2cn0jjx3yxruf14zkzk8zrybnksj3rlkup_sudedx20hjfybbnyd8jzsd5xv9eqfsrmhfhdbanv9c8gzmxknnr5otvlyfwvrob4osp3woy2eyxmm9g3qljft6j_jtycra7-7bnvize8jslctt0ch563kisfnqmxmkrwqhzahrcrrhwspg"  # noqa

SLEEPY_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMTEwMTcxOCwianRpIjoiMDM2YmNmZTktODg5OC00Nzg0LWIwYWQtZTRkOTczN2JjZjgxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InNsZWVweSIsIm5iZiI6MTYyMTEwMTcxOH0.OoHNM5l_p8n2OKz-IEondgHzUhHwXmPY0rWnXrto9WSkHEGOAL6Yqc37dancRUIzvvG2l_oK88O0eHJEFMPT0M0F-18wvCQ9wdQfiAUSiagFw4o_sUomHXu0xWjDFZ-gClUW-85qZiyKjx8gYvCYod1rehBy1B52kZ6DAd2tzQfwzI8ncgsjdsqGcOotkLisidGrqRA2jXqeJjPrwNQlHNl4OH7n7pxzzMb4_spyWEG12pjYZwa77oMDim_RjQpmo8RnNOEgenN9fGnBN3myluKY8AV7ZCat5vORzrKARWOj_-EQr6c6-9ZrxLWArEVkecB-WG6f5U8KmnUsrPq6Cg"  # NOQA

NOONE_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMTEwMTc1MywianRpIjoiZWVlODQ1MmMtZGJkYi00Njk1LWFmYWItNDhmZTQ2ZDNlYzE4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im5vb25lIiwibmJmIjoxNjIxMTAxNzUzfQ.HFfZFesk55Wi6ucUyjs3XR80giJhIvuK-9mrwJ0X0pvKqRGaa6kfPssZgO9LwrMsjRNClQVLdaHr12YTuMmPWAXj7glLvQeaGP60tfGhDacHJxIEQT1PyVdynGz66y4o13Gq32MY5zMXM4cFCy6-n0x6T-Gzrw5lJyn_wXGFeUE2rms19RZt4UrDLUXeKZlGUPyeMd34j23Io5IegrL4U5LLHvmP8IM9xZROcruJ87FLSZxHIdjg36YZ8oyTt7L8W-26fR6Ts_asyEpm0nOo8N1lszNPkx87f7Ckwyqoyom33nUIJUapDPR0LqYNd8bH_rp37Ed31zlAIU0L-hAipA"  # NOQA


def random_string(
    size=9,
    prefix="test_",
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
):
    return prefix + ''.join(random.choice(chars) for _ in range(size))


def randome_sqlite_uri(tmp_dir):
    # Only works on linux.
    fname = random_string() + ".sqlite"
    sqlite_uri = "sqlite:///" + os.path.join(tmp_dir, fname)

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
