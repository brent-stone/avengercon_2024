"""
Cumulative route from all API versions
"""

from fastapi import APIRouter
from avengercon.api.v1.route_hello import router as router_hello
from avengercon.api.v1.route_upload import router as router_upload

api_router_v1 = APIRouter(prefix="/v1")

api_router_v1.include_router(router_hello, prefix="/hello", tags=["Testing"])
api_router_v1.include_router(router_upload, prefix="/upload", tags=["Upload"])
