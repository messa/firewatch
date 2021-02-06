from aiohttp.web import Response, RouteTableDef, json_response


routes = RouteTableDef()


@routes.get('/')
async def index_handler(request):
    return Response(text='Hello! This is Firewatch server.\n')


@routes.get('/api/checks')
async def list_checks_handler(request):
    model = request.app['model']
    return json_response({
        'http_checks': [
            {
                'check_id': check.check_id,
                'url': check.url,
                'last_result': export_check_result(await model.get_last_check_result(check)),
            }
            for check in request.app['http_checks']
        ],
    })


@routes.get('/api/http-checks/{check_id}')
async def get_check_handler(request):
    model = request.app['model']
    check, = [ch for ch in request.app['http_checks'] if ch.check_id == request.match_info['check_id']]
    return json_response({
        'http_check': {
            'check_id': check.check_id,
            'url': check.url,
        },
    })


@routes.get('/api/http-checks/{check_id}/last-results')
async def get_check_handler(request):
    model = request.app['model']
    check, = [ch for ch in request.app['http_checks'] if ch.check_id == request.match_info['check_id']]
    return json_response({
        'last_results': [export_check_result(r) for r in await model.get_last_check_results(check)],
    })


def export_check_result(result):
    if not result:
        return None
    return {
        'time': result.time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'status_ok': result.status_ok,
        'total_duration': result.total_duration,
    }