import random
import string

import pytest

JWT_PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDV+7UTCb5JMX/GIY3g6kus84K5ko08nKbZcPgtRbTOkdNLFDcfotefNi+Y3bDEwMydXyc7uBmLkl9hyjBwTdCj6zAJ4VhLZ5wN0qg1cmg4Wkm6EUFgBHf7NY6V5M+v6XyZFinmzoe+J5llTH5xXLkieNMNtSDPUZWtRyhT9bwNSzYzBYZ13L1/yJJVUnb8mUmC2RG5ZqT8DZ+R/Y0Z35qACNmVqFTbSwFm3IoW2XcMXZawAKGoj0e9z6Eo6KZIRmVEFOfoeokz92zhS4b+j0+OJfmknpLYLHEyHswOnyFXFeNH1AHkGjDcAZwfr5ZMKpsy9XXlGiO2kFhK7RQ1ITvF olssont@n95996.nbi.ac.uk"  # NOQA

GRUMPY_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI5NjJjODEyNi1kZDJlLTQ1NDEtODQyOC0yZDYxYjEwZmU0M2YiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU1MzIyMzEzMywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU1MzIyMzEzMywiaWRlbnRpdHkiOiJncnVtcHkifQ.K1YYcUp2jfpBhVd7ggBJ_mpnQT_ZAGRjfgrReoz9no6zZ_5Hlgq2YLUNFtFfr2PrqsaO5fKWUfKrR8bjMijtlRlAEmyCJvalqXDWvriMf2QowyR6IjKxSNZcVCMkJXEk7cRlEM9f815YABc3RsG1F75n2dV5NSuvcQ4dQoItvNYpsuHZ3c-xYQuaQt7_Ch50Ez-H2fJatXQYdnHruyZOJQKPIssxU_yyeCnlOGklCmDn8mIolQEChrvW9HhpvgXsaAWEHjtNRK4T_ZH37Dq44fIB9ax6GGRZHDjWmjOicrGolfu73BuI8fOpLLpW5af6SKP-UhZA4AcW_TYG4PnOpQ"  # NOQA


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
