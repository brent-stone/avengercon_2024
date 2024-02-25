"""
FastAPI server initialization entrypoint
"""

from fastapi import FastAPI

from avengercon import __version__
from avengercon.api import api_router_v1
from avengercon.logger import logger
from avengercon.api.swagger import customize_swagger


def get_application() -> FastAPI:
    """
    Start the FastAPI server
    :return: An active FastAPI instance
    """

    _app = FastAPI(
        title="Avengercon",
        version=__version__,
        # Disable the automatic swagger docs
        docs_url=None,
    )
    # Enable locally hosted swagger js/css/favicon
    # Note: it's possible to do this with a FastAPI lifespan hook but that approach
    # causes more issues with Mypy type checking than it's worth.
    customize_swagger(_app)
    _app.include_router(api_router_v1)
    logger.info(f"FastAPI server starting. API version: {__version__}")

    return _app


# Note: This specific module name of "main" and object declaration of "app" are used by
# /entrypoints/start-reload.sh and start.sh
app = get_application()
