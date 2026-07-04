from aiohttp import web
import os

supflix_routes = web.RouteTableDef()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@supflix_routes.get("/supflix")
async def supflix_home(request):
    return web.FileResponse(
        os.path.join(BASE_DIR, "templates", "home.html")
    )