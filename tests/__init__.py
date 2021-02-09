import random
import string

import pytest

JWT_PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDV+7UTCb5JMX/GIY3g6kus84K5ko08nKbZcPgtRbTOkdNLFDcfotefNi+Y3bDEwMydXyc7uBmLkl9hyjBwTdCj6zAJ4VhLZ5wN0qg1cmg4Wkm6EUFgBHf7NY6V5M+v6XyZFinmzoe+J5llTH5xXLkieNMNtSDPUZWtRyhT9bwNSzYzBYZ13L1/yJJVUnb8mUmC2RG5ZqT8DZ+R/Y0Z35qACNmVqFTbSwFm3IoW2XcMXZawAKGoj0e9z6Eo6KZIRmVEFOfoeokz92zhS4b+j0+OJfmknpLYLHEyHswOnyFXFeNH1AHkGjDcAZwfr5ZMKpsy9XXlGiO2kFhK7RQ1ITvF olssont@n95996.nbi.ac.uk"  # NOQA


def random_string(
    size=9,
    prefix="test_",
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
):
    return prefix + ''.join(random.choice(chars) for _ in range(size))


@pytest.fixture
def tmp_app(request):

    from dtool_lookup_server import create_app, mongo, sql_db

    tmp_mongo_db_name = random_string()

    config = {
        "SECRET_KEY": "secret",
        "FLASK_ENV": "development",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
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

    @request.addfinalizer
    def teardown():
        mongo.cx.drop_database(tmp_mongo_db_name)
        sql_db.session.remove()

    return app.test_client()
