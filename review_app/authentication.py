import jwt
from jwt import PyJWKClient
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


def get_jwks_client():
    kc_url = settings.KEYCLOAK_CONFIG["URL"]
    realm = settings.KEYCLOAK_CONFIG["REALM"]

    if kc_url.endswith("/"):
        kc_url = kc_url[:-1]

    jwks_url = f"{kc_url}/realms/{realm}/protocol/openid-connect/certs"

    return PyJWKClient(jwks_url)


global_jwks_client = get_jwks_client()


class KeycloakAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                raise AuthenticationFailed(
                    "Authorization header must start with Bearer"
                )
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format")

        payload = self._decode_token(token)
        user = self._get_or_create_user(payload)

        return (user, None)

    def authenticate_header(self, _):
        return "Bearer"

    def _decode_token(self, token):
        try:
            signing_key = global_jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience="account",
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f"Invalid token: {str(e)}")
        except jwt.PyJWKClientError:
            raise AuthenticationFailed("Key identification failed")
        except jwt.InvalidAudienceError:
            raise AuthenticationFailed("Token audience mismatch")

    def _get_or_create_user(self, payload):
        keycloak_id = payload.get("sub")
        email = payload.get("email")

        if not keycloak_id or not email:
            raise AuthenticationFailed("Token must contain sub and email claims")

        realm_access = payload.get("realm_access", {})
        roles = realm_access.get("roles", [])

        try:
            user = User.objects.get(keycloak_id=keycloak_id)
        except User.DoesNotExist:
            user = User.objects.create_user(email=email, keycloak_id=keycloak_id)

        self._sync_permissions(user, roles)

        return user

    def _sync_permissions(self, user, roles):
        target_groups = []
        for role in roles:
            if not role.lower().startswith("book_"):
                continue

            group, _ = Group.objects.get_or_create(name=role.lower())
            target_groups.append(group)
        user.groups.set(target_groups)
