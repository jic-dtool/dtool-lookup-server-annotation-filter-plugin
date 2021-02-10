from flask import (
    Blueprint,
    abort,
    request,
    jsonify,
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from dtool_lookup_server import (
    AuthenticationError
)

from dtool_lookup_server_annotation_filter_plugin.utils import (
    get_annotation_key_info_by_user,
    get_annotation_value_info_by_user,
)


annotation_filter_bp = Blueprint(
    'annotation_filter_plugin',
    __name__,
    url_prefix="/annotation_filter_plugin"
)


@annotation_filter_bp.route('/keys', methods=["POST"])
@jwt_required
def keys():
    username = get_jwt_identity()
    query = request.get_json()
    try:
        data = get_annotation_key_info_by_user(username, query)
    except AuthenticationError:
        abort(401)
    return jsonify(data)


@annotation_filter_bp.route('/annotation_values', methods=["POST"])
@jwt_required
def annotation_values():
    username = get_jwt_identity()
    query = request.get_json()
    try:
        data = get_annotation_value_info_by_user(username, query)
    except AuthenticationError:
        abort(401)
    return jsonify(data)
