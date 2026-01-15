# -*- coding: utf-8 -*-

import os
import re

import uvicorn

from settings import settings


def main():
    from application import app

    if match := re.match(r"sqlite://(.*)", settings.database.url):
        dirname = os.path.dirname(match.group(1))
        os.makedirs(dirname, exist_ok=True)

    uvicorn.run(
        app,
        host=settings.server.host,
        port=settings.server.port,
        access_log=settings.server.access_log,
    )


if __name__ == "__main__":
    main()
