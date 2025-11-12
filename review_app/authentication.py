import jwt
from jwt import PyJWKClient
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class KeycloakAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                raise AuthenticationFailed('Authorization header must start with Bearer')
        except ValueError:
            raise AuthenticationFailed('Invalid Authorization header format')

        payload = self._decode_token(token)
        user = self._get_or_create_user(payload)

        return (user, None)

    def _decode_token(self, token):
        url = f"{settings.KEYCLOAK_CONFIG['URL']}/realms/{settings.KEYCLOAK_CONFIG['REALM']}/protocol/openid-connect/certs"
        jwks_client = PyJWKClient(url)

        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience="account",
                options={"verify_aud": False}
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')

    def _get_or_create_user(self, payload):
        keycloak_id = payload.get('sub')
        email = payload.get('email')

        if not keycloak_id or not email:
            raise AuthenticationFailed('Token must contain sub and email claims')

        realm_access = payload.get('realm_access', {})
        roles = realm_access.get('roles', [])

        try:
            user = User.objects.get(keycloak_id=keycloak_id)
            if user.email != email:
                user.email = email
                user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                keycloak_id=keycloak_id
            )

        self._sync_permissions(user, roles)

        return user

    def _sync_permissions(self, user, roles):
        self._map_permissions("BOOK_ADMIN", roles, user)
        self._map_permissions("BOOK_USER", roles, user)

    def _map_permissions(self, role_name, roles, user):
        if role_name in roles:
            group, _ = Group.objects.get_or_create(name=role_name.lower())
            if group not in user.groups.all():
                user.groups.add(group)
        else:
            group = Group.objects.filter(name=role_name.lower()).first()
            if group and group in user.groups.all():
                user.groups.remove(group)