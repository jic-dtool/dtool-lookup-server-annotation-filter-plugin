from setuptools import setup

setup(
    name="dtool-lookup-server-annotation-filter-plugin",
    packages=["dtool_lookup_server_annotation_filter_plugin"],
    install_requires=[
        "flask",
        "dtool-lookup-server",
    ],
    entry_points={
        "dtool_lookup_server.blueprints": [
            "dtool_lookup_server_annotation_filter_plugin=dtool_lookup_server_annotation_filter_plugin:annotation_filter_bp",  # NOQA
        ],
    }
)
