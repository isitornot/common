Support Middleware
==================
This contains various add-in and support utilities useful for multiple components.

JWT Auth
--------
Middleware and basic support templates and examples for authentication and profile viewing with Auth0.
Auth0 client codes should be set in env vars or secure storage.

Getting Started
---------------
You need python 3.6.x which can be installed with anaconda, brew, etc.
1) Create a virtual env
   `python -m venv .env`
2) Activate the env
   `source .env/bin/activate`
3) Create a `local_config` file
```
AUTH0 = {
    'CLIENT_SECRET': 'PUT_YOUR_AUTH0_CLIENT_SECRET_HERE',
    'CLIENT_ID': 'PUT_YOUR_AUTH0_CLIENT_ID_HERE',
    'REDIRECT_URL': 'http://localhost:9000/auth_callback',
    'DOMAIN': 'PUT.YOUR.AUTH0.DOMAIN.HERE'
}
```
4) Run the sample server
   `CONFIG_FILE=local_config ./main.py`
5) Browse to <http://localhost:9000/>

Getting Started with Docker
---------------------------
Build the image in `common` and execute with a `local_config` volume mounted to the container
and `CONFIG_FILE` pointing to the volume mount location.
