"""API routing for URL entities."""

from flask import Blueprint, Response, abort, jsonify
from flask.views import MethodView

from url_tribunal.api.v1.dependencies import get_db_session
from url_tribunal.api.v1.schemas.url import UrlSchema
from url_tribunal.db.repositories.url import UrlRepository
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

            response = UrlSchema(
                id=url.id,
                hash=url.url_hash,
                full_url=url.full_url,
                verdict=url.verdict,
                confidence=url.verdict_confidence,
                last_scanned_at=url.last_scanned_at,
            )

            return jsonify(response.model_dump()), 200


url_bp.add_url_rule(
    '/<string:url_hash>',
    view_func=Urls.as_view('urls'),
    methods=['GET'],
)
