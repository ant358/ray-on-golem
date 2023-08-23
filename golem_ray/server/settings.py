import os
from pathlib import Path

import dotenv
from yarl import URL

dotenv.load_dotenv()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
        }
    },
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "aiohttp": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "golem_ray": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

YAGNA_PATH = Path(os.getenv("YAGNA_PATH", "yagna"))
YAGNA_APPKEY = os.getenv("YAGNA_APPKEY")
GCS_REVERSE_TUNNEL_PORT = int(os.getenv("GCS_REVERSE_TUNNEL_PORT", 3009))
PROXY_URL = URL(os.getenv("PROXY_URL", "proxy.dev.golem.network"))
SERVER_BASE_URL = URL(os.getenv("SERVER_BASE_URL", "http://localhost:8080"))

URL_CREATE_CLUSTER = "/create_cluster"
URL_GET_NODES = "/"
URL_IS_RUNNING = "/is_running"
URL_IS_TERMINATED = "/is_terminated"
URL_NODE_TAGS = "/tags"
URL_INTERNAL_IP = "/internal_ip"
URL_SET_NODE_TAGS = "/set_tags"
URL_CREATE_NODES = "/create_nodes"
URL_TERMINATE_NODES = "/terminate"
URL_GET_NODE_SSH_PORT = "/node_port"
