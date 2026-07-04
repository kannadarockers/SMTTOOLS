from aiohttp import web
from .template_engine import env

supflix_routes = web.RouteTableDef()

@supflix_routes.get("/supflix")
async def supflix_home(request):
    template = env.get_template("home.html")
    html = template.render()

    return web.Response(
        text=html,
        content_type="text/html"
    )