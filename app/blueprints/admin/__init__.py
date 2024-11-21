from .committees_api import committees_api
from .criteria_api import criteria_api
from .directions_api import direction_api
from .puncts_api import puncts_api
from .routes import admin_bp
from .subcriteria_api import subcriteria_api

admin_bp.register_blueprint(committees_api, url_prefix="/api")
admin_bp.register_blueprint(criteria_api, url_prefix="/api")
admin_bp.register_blueprint(direction_api, url_prefix="/api")
admin_bp.register_blueprint(puncts_api, url_prefix="/api")
admin_bp.register_blueprint(subcriteria_api, url_prefix="/api")

__all__ = [
    "admin_bp"
]
