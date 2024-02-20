"""
Swagger UI customization
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from starlette.responses import HTMLResponse


def customize_swagger(a_app: FastAPI) -> None:
    """
    Override default swagger UI to use local static javascript, CSS, and favicon
    https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/
    https://fastapi.tiangolo.com/advanced/events/

    Args:
        a_app: An initialized FastAPI object

    Returns: Mutated FastAPI object

    """

    a_app.mount(
        path="/static",
        app=StaticFiles(directory="/app/avengercon/static"),
        name="static",
    )

    @a_app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        """
        Override default swagger UI to use local assets
        Returns: HTML response of Swagger UI

        """
        return get_swagger_ui_html(
            openapi_url=str(a_app.openapi_url),
            title=a_app.title + " - Swagger UI",
            oauth2_redirect_url=a_app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
            swagger_favicon_url="/static/favicon_cyber.png",
        )

    @a_app.get(str(a_app.swagger_ui_oauth2_redirect_url), include_in_schema=False)
    async def swagger_ui_redirect() -> HTMLResponse:
        """
        Override default swagger behavior
        Returns: OAuth2 redirect HTML

        """
        return get_swagger_ui_oauth2_redirect_html()
