"""
This module configures the BlackSheep application before it starts.
"""
from blacksheep import Application
from blacksheep.server.csrf import use_anti_forgery
from blacksheep.server.diagnostics import get_diagnostic_app
from rodi import Container

from app.errors import configure_error_handlers
from app.services import configure_services
from app.settings import Settings
from app.templating import configure_templating

import env


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    app = Application(services=services)
    app.serve_files("app/static")
    app.use_sessions(
        secret_key=env.SECRET_KEY,
        session_cookie=env.SESSION_COOKIE
    )
    configure_error_handlers(app)
    configure_templating(app, settings)
    use_anti_forgery(app)
    return app


def get_app():
    try:
        return configure_application(*configure_services())
    except Exception as exc:
        return get_diagnostic_app(exc)


app = get_app()
