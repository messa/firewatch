from aiohttp.web import Response, RouteTableDef, json_response


routes = RouteTableDef()


@routes.get('/')
async def index_handler(request):
    return Response(text='Hello! This is Firewatch server.\n')


@routes.get('/api/checks')
async def list_checks_handler(request):
    return json_response({
        'http_checks': [
            {
                'url': check.url,
            }
            for check in request.app['http_checks']
        ],
    })
