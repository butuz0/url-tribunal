"""API routing for URL entities."""

from flask import Blueprint, Response, abort, jsonify
from flask.views import MethodView

from url_tribunal.api.v1.schemas import ScanSchema, UrlSchema
from url_tribunal.db.repositories import ScanRepository
from url_tribunal.db.repositories import UrlRepository
from url_tribunal.db.session import get_db_session
from url_tribunal.utils import like_sha256

url_bp = Blueprint('urls', __name__, url_prefix='/api/v1/urls')


class Urls(MethodView):
    """Endpoints for managing URL resources."""

    def get(self, url_hash: str) -> tuple[Response, int]:
        """Fetch a URL record by its SHA-256 hash."""

        if not like_sha256(url_hash):
            abort(400, 'url_hash must be a valid SHA256 string.')

        with get_db_session() as session:
            url = UrlRepository(session).get_by_hash(url_hash)

            if url is None:
                abort(404, description='Target URL string hash not found.')

            response = UrlSchema.model_validate(url)
            return jsonify(response.model_dump()), 200


class UrlScans(MethodView):
    """Endpoints for managing Scan history of URLs."""

    def get(self, url_hash: str) -> tuple[Response, int]:
        """Fetch all Scans for a URL record by its SHA-256 hash."""

        if not like_sha256(url_hash):
            abort(400, 'url_hash must be a valid SHA256 string.')

        with get_db_session() as session:
            scans = ScanRepository(session).list_by_url_hash(url_hash)

            response = [ScanSchema.model_validate(s).model_dump() for s in scans]
            return jsonify(response), 200


url_bp.add_url_rule(
    '/<string:url_hash>',
    view_func=Urls.as_view('urls'),
    methods=['GET'],
)

url_bp.add_url_rule(
    '/<string:url_hash>/scans',
    view_func=UrlScans.as_view('url_scans'),
    methods=['GET'],
)
