from aiohttp import web
from .route import routes
from .studio import studio_routes
from supflix.routes import supflix_routes
import os

async def web_server():
    web_app = web.Application(client_max_size=30000000)

    web_app.router.add_static(
        "/static/",
        path=os.path.join(os.getcwd(), "supflix", "static"),
        name="static"
    )

    web_app.add_routes(supflix_routes)
    web_app.add_routes(studio_routes)
    web_app.add_routes(routes)

    return web_app 