#!/usr/bin/env python


from sanic import Sanic
from sanic_session import InMemorySessionInterface
from sanic_openapi import swagger_blueprint, openapi_blueprint
from jwt_auth import blueprint_jwt


DEFAULT_CONFIG = {
    'AUTH0': {
        'CLIENT_SECRET': 'INVALID_SECRET',
        'CLIENT_ID': 'INVALID_CLIENT_ID',
        'REDIRECT_URL': 'http://localhost:9000/auth_callback',
        'DOMAIN': 'USER.auth0.com'
    }
}


app = Sanic(__name__)
app.config.update(DEFAULT_CONFIG)
app.config.from_envvar('CONFIG_FILE')
app.static('/', './static/index.html')
app.static('/css', './static/css')
app.static('/js', './static/js')
app.static('/images', './static/images')
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)
session_interface = InMemorySessionInterface()


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    await session_interface.open(request)


@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    if response:
        await session_interface.save(request, response)


app.blueprint(blueprint_jwt)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9000', debug=True)
