'''
Google login
------------

1. Go to https://console.cloud.google.com/apis/credentials
2. Click "+ Create credentials", select "OAuth client ID"
3. Under "Authorized redirect URIs", add "http://localhost:8000/api/auth/google-callback"
4. Copy "Client ID" and "Client secret" into Firewatch configuration
'''

from aiohttp.web import Response, FileResponse, RouteTableDef, json_response, HTTPFound
from aiohttp_session import get_session, new_session
from asyncio import get_running_loop
from functools import partial
from logging import getLogger
from requests_oauthlib import OAuth2Session

try:
    from asyncio import to_thread
except ImportError:
    async def to_thread(func, *args, **kwargs):
        loop = get_running_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))


logger = getLogger(__name__)

routes = RouteTableDef()


@routes.get('/api/auth/login-methods')
async def logout_handler(request):
    conf = request.app['conf']
    return json_response({
        'login_methods': {
            'dev': bool(conf.auth.dev_login_enabled),
            'google': bool(conf.auth.google_client_id and conf.auth.google_client_secret),
        },
    })


@routes.get('/api/auth/dev')
async def dev_login_handler(request):
    session = await new_session(request)
    conf = request.app['conf']
    if not conf.auth.dev_login_enabled:
        return Response(text='Development login not enabled\n', status=403)
    session['dev_login'] = True
    session['user'] = {
        'email': 'user@example.com',
    }
    return HTTPFound(location='/dashboard')


@routes.get('/api/auth/google')
async def google_login_handler(request):
    conf = request.app['conf']

    redirect_uri = conf.auth.google_redirect_uri
    if not redirect_uri:
        if request.headers.get('referer') == 'http://localhost:3000/login':
            # we are proxied through Next.js dev server
            redirect_uri = 'http://localhost:3000/api/auth/google-callback'
        else:
            redirect_uri = f"{request.url}-callback"
    logger.debug('redirect_uri: %r', redirect_uri)

    if not conf.auth.google_client_id or not conf.auth.google_client_secret:
        return Response(text='Google auth not configured\n', status=500)

    def sync_code(conf):
        oauth = OAuth2Session(
            conf.auth.google_client_id,
            redirect_uri=redirect_uri,
            scope=conf.auth.google_scope)
        authorization_url, state = oauth.authorization_url(
            conf.auth.google_authorization_base_url,
            # access_type and prompt are Google specific extra parameters.
            access_type="offline", prompt="select_account")
        return authorization_url, state

    authorization_url, state = await to_thread(sync_code, conf=conf)
    logger.debug('Google authorization_url: %s', authorization_url)

    session = await new_session(request)
    session['google_state'] = state
    session['google_redirect_uri'] = redirect_uri

    return HTTPFound(location=authorization_url)


@routes.get('/api/auth/google-callback')
async def google_login_callback_handler(request):
    conf = request.app['conf']

    session = await get_session(request)
    if session['google_state'] != request.query['state']:
        logger.info('State mismatch')
        raise HTTPFound(location='/login')

    def sync_code(conf, code):
        oauth = OAuth2Session(
            conf.auth.google_client_id,
            redirect_uri=session['google_redirect_uri'],
            scope=conf.auth.google_scope)

        token = oauth.fetch_token(
            conf.auth.google_fetch_token_url,
            client_secret=conf.auth.google_client_secret,
            code=code)
        r = oauth.get(conf.auth.google_user_info_url)
        r.raise_for_status()
        me = r.json()
        return token, me

    try:
        token, me = await to_thread(sync_code, conf=conf, code=request.query['code'])
    except Exception as e:
        logger.info('Processing Google callback failed: %r', e)
        raise HTTPFound(location='/login')

    #logger.debug('Google token: %r', token)
    #logger.debug('Google me: %r', me)

    if not me['verified_email']:
        return Response(text='Google returned user info with unverified e-mail\n', status=403)

    session = await new_session(request)
    session['user'] = me
    session['google_token'] = token
    return HTTPFound(location='/dashboard')


@routes.get('/api/auth/logout')
async def logout_handler(request):
    session = await get_session(request)
    session['user'] = None
    session['google_token'] = None
    # TODO: invalidate the google token on google api?
    return HTTPFound(location='/login')


@routes.get('/api/user')
async def dashboard_handler(request):
    session = await get_session(request)
    return json_response({'user': session.get('user')})
