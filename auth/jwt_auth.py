from functools import wraps
from sanic import Blueprint, response, exceptions
from sanic_jinja2 import SanicJinja2
import aiohttp
import json
import jwt


blueprint_jwt = Blueprint('jwt_auth')
jinja = SanicJinja2()


class AuthException(exceptions.SanicException):
    status_code = 401


def requires_auth(f):
    @wraps(f)
    def decorated(request, *args, **kwargs):
        if 'Authentication' not in request['session']:
            raise AuthException({'code': 'authorization_required',
                                 'description': 'A user must be logged in and authorized.'})
        return f(request, *args, **kwargs)
    return decorated


@blueprint_jwt.middleware('request')
async def unpack_auth(request):
    if 'session' in request and 'Authentication' in request['session']:
        user_info = jwt.decode(request['session']['Authentication'].split()[1],
                               key=request.app.config.AUTH0['CLIENT_SECRET'],
                               audience=request.app.config.AUTH0['CLIENT_ID'])
        if user_info:
            request['user_info'] = user_info


@blueprint_jwt.listener('after_server_start')
async def setup_jinja(app, loop):
    jinja.init_app(app)


@blueprint_jwt.route('/login')
async def login(request):
    """Login to auth0
    """
    if 'Authentication' not in request['session']:
        return jinja.render('login.html', request, config=request.app.config.AUTH0)
    return response.redirect(request.app.url_for('jwt_auth.profile'))


@blueprint_jwt.route('/logout')
async def logout(request):
    """Logout of the session.
    """
    if 'Authentication' in request['session']:
        del request['session']['Authentication']
    return response.redirect('/')


@blueprint_jwt.route('/auth_callback', methods=['GET', 'POST'])
async def auth_callback(request):
    """Populate auth and profile data
    """
    code = request.args.get('code')
    if not code:
        code = request.form.get('code')
    json_header = {'content-type': 'application/json'}
    token_url = "https://{domain}/oauth/token".format(domain=request.app.config.AUTH0['DOMAIN'])
    token_payload = {
        'client_id': request.app.config.AUTH0['CLIENT_ID'],
        'client_secret': request.app.config.AUTH0['CLIENT_SECRET'],
        'redirect_uri': request.app.config.AUTH0['REDIRECT_URL'],
        'code': code,
        'grant_type': 'authorization_code'
    }
    async with aiohttp.ClientSession() as client:
        async with client.post(token_url, data=json.dumps(token_payload), headers=json_header) as resp:
            token_info = await resp.json()
        request['session']['Authentication'] = '{} {}'.format(token_info["token_type"], token_info["id_token"])
    return response.redirect(request.app.url_for('jwt_auth.profile'))


@blueprint_jwt.route('/profile')
async def profile(request):
    if 'user_info' not in request:
        return response.redirect(request.app.url_for('jwt_auth.login'))
    return jinja.render('profile.html', request, user=request['user_info'])
