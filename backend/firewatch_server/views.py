from aiohttp.web import Response, RouteTableDef


routes = RouteTableDef()


@routes.get('/')
async def index_handler(request):
    return Response(text='Hello! This is Firewatch server.\n')
