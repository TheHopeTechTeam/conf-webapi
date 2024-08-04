"""
main application
"""
import firebase_admin
from fastapi import FastAPI, Request, status, HTTPException, Response
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from firebase_admin import credentials

from app.config import settings
from app.containers import Container
from app.libs.utils.lifespan import lifespan
from app.routers import api_router


__all__ = ["app"]


def register_router(application: FastAPI) -> None:
    """
    register router
    :param application:
    :return:
    """
    application.include_router(api_router, prefix="/api")


def register_middleware(application: FastAPI) -> None:
    """
    register middleware
    :param application:
    :return:
    """


def init_firebase():
    """
    init firebase
    :return:
    """
    cred = credentials.Certificate(settings.GOOGLE_FIREBASE_CERTIFICATE)
    firebase_admin.initialize_app(cred)


def get_application() -> FastAPI:
    """
    get application
    """
    application = FastAPI(lifespan=lifespan)
    # set route class
    # application.router.route_class = LogRouting
    # set container
    container = Container()
    application.container = container

    init_firebase()
    register_middleware(application=application)
    register_router(application=application)

    return application


app = get_application()


@app.middleware("http")
async def http_middleware_handler(request: Request, callback):
    """

    :param request:
    :param callback:
    :return:
    """
    try:
        response: Response = await callback(request)
        return response
    finally:
        container: Container = request.app.container
        container.reset_singletons()


# @app.exception_handler(InvalidAuthorizationToken)
# def on_invalid_token(
#     request: Request,
#     exc: InvalidAuthorizationToken
# ):
#     """
#
#     :param request:
#     :param exc:
#     :return:
#     """
#     return JSONResponse(
#         content={"detail": str(exc)},
#         status_code=status.HTTP_401_UNAUTHORIZED
#     )


@app.exception_handler(HTTPException)
async def root_http_exception_handler(request, exc: HTTPException):
    """

    :param request:
    :param exc:
    :return:
    """
    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc):
    """

    :param request:
    :param exc:
    :return:
    """
    content = {
        "detail": {
            "message": "Internal Server Error",
            "url": str(request.url)
        }
    }
    if settings.ENV != "prod":
        content["debug_detail"] = f"{exc.__class__.__name__}: {exc}"
    return JSONResponse(
        content=content,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
