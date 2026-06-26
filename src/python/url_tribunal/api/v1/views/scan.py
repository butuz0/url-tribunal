"""API routing for Scan entities."""

from flask import Blueprint, Response, abort, jsonify
from flask.views import MethodView

from url_tribunal.api.v1.schemas import ScanDetailSchema
from url_tribunal.db.repositories import ScanRepository
from url_tribunal.db.session import get_db_session

scan_bp = Blueprint('scans', __name__, url_prefix='/api/v1/scans')


class Scans(MethodView):
    """Endpoints for managing Scan resources."""

    def get(self, scan_id: int) -> tuple[Response, int]:
        """Fetch a Scan record with provider results by its id."""

        with get_db_session() as session:
            scan = ScanRepository(session).get_with_providers(scan_id)

            if scan is None:
                abort(404, f'Scan with id {scan_id} not found.')

            response = ScanDetailSchema.model_validate(scan)
            return jsonify(response.model_dump()), 200


scan_bp.add_url_rule(
    '/<int:scan_id>',
    view_func=Scans.as_view('scans'),
    methods=['GET'],
)
