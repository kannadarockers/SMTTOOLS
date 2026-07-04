from aiohttp import web
from .template_engine import env
import traceback

supflix_routes = web.RouteTableDef()

@supflix_routes.get("/supflix")
async def supflix_home(request):
    try:
        template = env.get_template("home.html")
        html = template.render()
        return web.Response(
            text=html,
            content_type="text/html"
        )
    except Exception:
        return web.Response(
            text=traceback.format_exc(),
            content_type="text/plain"
        )