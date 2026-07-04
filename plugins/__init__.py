from aiohttp import web
from .route import routes
from .studio import studio_routes

async def web_server():
    web_app = web.Application(client_max_size=30000000)

    web_app.add_routes(routes)
    web_app.add_routes(studio_routes)

    return web_app
