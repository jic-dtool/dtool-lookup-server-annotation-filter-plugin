"""Utility functions."""

from dtool_lookup_server import (
    mongo,
    MONGO_COLLECTION,
)

from dtool_lookup_server.utils import (
    get_user_obj,
    preprocess_query_base_uris,
)

VALID_MONGO_QUERY_KEYS = (
    "base_uris",
)
ALLOWED_TYPES = (str, int, float, bool)


def filter_dict_to_mongo_query(filters):
    """Return mongo query from filters dict."""
    base_uri_subquery = None
    if len(filters["base_uris"]) == 1:
        base_uri_subquery = str(filters["base_uris"][0])
    else:
        base_uris = [str(b) for b in filters["base_uris"]]
        base_uri_subquery = {"$in": base_uris}

    return {"base_uri": base_uri_subquery}


def get_annotation_key_info_by_user(username, filters):
    """Return dictionary with annotation keys and numbers of datasets
    given that key and any filters passed into the function.

    :param username: username
    :param filters: dictionary with filters
    :returns: dictionary where keys are annotation keys and values
              are the numbers of datasets with that key given the
              filter provided
    """
    # Validate the user; raises AuthenticationError if invalid.
    get_user_obj(username)

    filters = preprocess_query_base_uris(username, filters)
    mongo_query = filter_dict_to_mongo_query(filters)

    # If there are no base URI the user has not got permissions to view any
    # datasets.
    if len(filters["base_uris"]) == 0:
        return {}

    cx = mongo.db[MONGO_COLLECTION].find(
        mongo_query,
        {
            "annotations": True,
        }
    )

    # There is probably a more clever way to do this using the
    # mongo query language.
    annotation_key_info = {}
    for ds in cx:

        # Create set of valid keys in dataset.
        ds_valid_keys = set()
        for key, value in ds["annotations"].items():
            if type(value) not in ALLOWED_TYPES:
                continue
            ds_valid_keys.add(key)

        # If the "annotation_key" filter is on check that key is part of it.
        if "annotation_keys" in filters:
            annotation_keys_set = set(filters["annotation_keys"])
            if len(annotation_keys_set.intersection(ds_valid_keys)) == 0:
                continue

        # If the "annotations" filter is on check that the key/value pair is
        # present, if not skip the dataset.
        skip = False
        if "annotations" in filters:
            print("annotations in filter")
            for ann_key, ann_value in filters["annotations"].items():
                print(f"ann_key {ann_key}, ds_valid_keys {ds_valid_keys}")
                if ann_key not in ds_valid_keys:
                    skip = True
                    break
                if ds["annotations"][ann_key] != ann_value:
                    skip = True
                    break
        if skip:
            continue

        # Add the key information.
        for key in ds_valid_keys:
            annotation_key_info[key] = annotation_key_info.get(key, 0) + 1

    return annotation_key_info
