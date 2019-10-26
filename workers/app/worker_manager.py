#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import sys
import argparse

from common import logger
from common.constants import DEFAULT_WEB_API_URL, DEFAULT_SOCKET_URI, WORKER_MANAGER
from manager.worker import WorkerManager


def main():
    parser = argparse.ArgumentParser(prog=WORKER_MANAGER)

    parser.add_argument(
        "--webapi-uri",
        help="zimfarm API URI",
        required=not bool(DEFAULT_WEB_API_URL),
        default=DEFAULT_WEB_API_URL,
        dest="webapi_uri",
    )

    parser.add_argument(
        "--socket-uri",
        help="zimfarm websocket URI (tcp://hostname:port)",
        required=not bool(DEFAULT_SOCKET_URI),
        default=DEFAULT_SOCKET_URI,
        dest="socket_uri",
    )

    parser.add_argument(
        "--username",
        help="username to authenticate to zimfarm",
        required=not bool(os.getenv("USERNAME")),
        default=os.getenv("USERNAME"),
    )

    parser.add_argument(
        "--password",
        help="password to authenticate to zimfarm",
        required=not bool(os.getenv("PASSWORD")),
        default=os.getenv("PASSWORD"),
    )

    parser.add_argument(
        "--workdir",
        help="directory in which workers create task-related files",
        required=not bool(os.getenv("WORKDIR")),
        default=os.getenv("WORKDIR"),
        dest="workdir",
    )

    args = parser.parse_args()

    logger.info(f"starting zimfarm {WORKER_MANAGER}.")
    try:
        manager = WorkerManager(
            username=args.username,
            password=args.password,
            webapi_uri=args.webapi_uri,
            socket_uri=args.socket_uri,
            workdir=args.workdir,
        )
        sys.exit(manager.run())
    except Exception as exc:
        logger.error(f"Unhandled exception: {exc}")
        logger.exception(exc)
        logger.error("exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
