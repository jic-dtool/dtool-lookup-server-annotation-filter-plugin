from flask import Blueprint

annotation_filter_bp = Blueprint(
    'annotation_filter_plugin',
    __name__,
    url_prefix="/annotation_filter_plugin"
)


@annotation_filter_bp.route('/keys', methods=["POST"])
def keys():
    return {"color": 2, "pattern": 2}
