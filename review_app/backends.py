from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.models import Group


class CustomKeycloakBackend(OIDCAuthenticationBackend):
    def filter_users_by_claims(self, claims):
        keycloak_id = claims.get("sub")
        if not keycloak_id:
            return self.UserModel.objects.none()

        try:
            return self.UserModel.objects.filter(keycloak_id=keycloak_id)
        except self.UserModel.DoesNotExist:
            return self.UserModel.objects.none()

    def create_user(self, claims):
        email = claims.get("email")
        keycloak_id = claims.get("sub")

        new_user = self.UserModel.objects.create_user(
            email=email,
            keycloak_id=keycloak_id,
        )

        self._sync_permissions(new_user, claims)
        return new_user

    def update_user(self, user, claims):
        self._sync_permissions(user, claims)
        return user

    def _sync_permissions(self, user, claims):
        realm_access = claims.get("realm_access", {})
        roles = realm_access.get("roles", [])

        target_groups = []
        for role in roles:
            if not role.lower().startswith("book_"):
                continue

            group, _ = Group.objects.get_or_create(name=role.lower())
            target_groups.append(group)

        user.groups.set(target_groups)
