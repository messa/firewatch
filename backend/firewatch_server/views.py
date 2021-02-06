from aiohttp.web import Response, FileResponse, RouteTableDef, json_response
from logging import getLogger


logger = getLogger(__name__)

routes = RouteTableDef()


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


allowed_static_path_characters = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/_-.')

@routes.get('/')
@routes.get('/{path:.+}')
def static_handler(request):
    url_path = request.match_info.get('path', 'index.html')
    conf = request.app['conf']
    if not conf.html_dir or not conf.html_dir.is_dir():
        logger.info('conf.html_dir: %s', conf.html_dir)
        return Response(text='html_dir is not configured or does not exist\n', status=500)
    if '..' in url_path or not (set(url_path) <= allowed_static_path_characters):
        logger.info('URL path contains unsupported characters: %r', url_path)
        return Response(text='URL path contains unsupported characters\n', status=403)
    src_path = (conf.html_dir / url_path).resolve()
    if not src_path.exists():
        alt_path = src_path.with_name(src_path.name + '.html')
        if alt_path.is_file():
            src_path = alt_path
    if not str(src_path).startswith(str(conf.html_dir)) or not src_path.relative_to(conf.html_dir):
        return Response(text='Forbidden\n', status=403)
    if src_path.is_dir():
        return Response(text='Directory listing forbidden\n', status=403)
    if src_path.is_file():
        logger.debug('Serving static file: %s', src_path)
        return FileResponse(src_path)
    return Response(text='File not found\n', status=404)


def export_check_result(result):
    if not result:
        return None
    return {
        'time': result.time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'status_ok': result.status_ok,
        'total_duration': result.total_duration,
    }