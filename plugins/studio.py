from aiohttp import web

studio_routes = web.RouteTableDef()

@studio_routes.get("/studio")
async def studio_home(request):
    return web.Response(
        text="<h1>🚀 Welcome to SMTTOOLS Studio</h1>",
        content_type="text/html"
    )
