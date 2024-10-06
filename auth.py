import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from settings import AUTH0_DOMAIN, ALGORITHMS,API_AUDIENCE


"""
https://fsnd-kml.auth0.com/authorize?audience=capstone&response_type=token&client_id=QgmGth71OqndSVlCJ6YIAFir6t2EAt48&redirect_uri=http://localhost:8100/login-results
https://fsnd-kml.auth0.com/.well-known/jwks.json
"""

#AUTH0_DOMAIN = 'dev-2jdum4ss1zy7wwvk.us.auth0.com'
#AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
#ALGORITHMS = ['RS256']
#API_AUDIENCE = 'flask_app'
#API_AUDIENCE = 'dev'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    req = request.headers.get('Authorization') # get Authorization in request
    try:
        if req is None:
           raise AuthError({
               'code': 'authorization_header_missing',
               'description': 'Authorization header is not exist.'
           }, 401)
        token = req.split() # get token
        if token[0].lower() != 'bearer':
           raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)
        if len(token) != 2:
           raise AuthError({
               'code': 'authorization_header_missing',
               'description': 'Authorization header is expected.'
           }, 401)
        return token[1]
    except:
        raise Exception('Not Implemented')


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string
    is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    try:
        if permission not in  payload['scope']:
            raise AuthError({
                'code': 'authorization_header_missing',
                'description': 'not have permission.'
            }, 401)
    except:
        raise AuthError({
                'code': 'authorization_header_missing',
                'description': 'not have permission.'
            }, 401)


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Invalid JWT header.'
        }, 401)

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed: No Key ID (kid).'
        }, 401)

    rsa_key = next(
        (key for key in jwks['keys'] if key['kid'] == unverified_header['kid']),
        None
    )

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception as e:
            raise AuthError({
                'code': 'invalid_token',
                'description': f'Unable to parse authentication token: {str(e)}'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)



'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims
    and check the requested permission
    return the decorator which passes the decoded payload
    to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
