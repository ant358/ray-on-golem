import argparse
import logging
import logging.config
from pathlib import Path

from aiohttp import web

from golem_ray.server.middlewares import error_middleware
from golem_ray.server.services import GolemService, RayService, YagnaService
from golem_ray.server.settings import (
    GOLEM_RAY_REVERSE_TUNNEL_PORT,
    LOGGING_CONFIG,
    PROXY_URL,
    WEBSOCAT_PATH,
    YAGNA_PATH,
)
from golem_ray.server.views import routes

logger = logging.getLogger(__name__)


def parse_sys_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Golem Ray's webserver.")
    parser.add_argument("port", type=int, help="port which be used for webserver to listen to")
    return parser.parse_args()


def prepare_tmp_dir():
    try:
        Path("/tmp/golem").mkdir(parents=True, exist_ok=True)
    except OSError:
        pass


async def print_hello(app: web.Application) -> None:
    logger.info("Server started")


def create_application() -> web.Application:
    app = web.Application(middlewares=[error_middleware])

    app["yagna_service"] = YagnaService(
        yagna_path=YAGNA_PATH,
    )

    app["golem_service"] = GolemService(
        golem_ray_reverse_tunnel_port=GOLEM_RAY_REVERSE_TUNNEL_PORT,
        proxy_url=PROXY_URL,
        websocat_path=WEBSOCAT_PATH,
    )

    app["ray_service"] = RayService(
        golem_service=app["golem_service"],
    )

    app.add_routes(routes)
    app.cleanup_ctx.append(golem_ray_ctx)
    app.on_startup.append(print_hello)

    return app


async def golem_ray_ctx(app: web.Application):
    yagna_service: YagnaService = app["yagna_service"]
    golem_service: GolemService = app["golem_service"]

    await yagna_service.init()
    await golem_service.init(yagna_appkey=yagna_service.yagna_appkey)

    yield  # before yield called on startup, after yield called on cleanup

    await golem_service.shutdown()
    await yagna_service.shutdown()


def main():
    logging.config.dictConfig(LOGGING_CONFIG)

    args = parse_sys_args()
    prepare_tmp_dir()

    app = create_application()
    web.run_app(app, port=args.port)


if __name__ == "__main__":
    main()
