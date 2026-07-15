import logging
from urllib.parse import parse_qs
from channels.auth import AuthMiddlewareStack
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

class JWTAuthMiddlewareWSGI(MiddlewareMixin):
    def process_request(self, request):
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token.split("Bearer ")[1]
            try:
                access_token = AccessToken(token)
                User = get_user_model()
                user = User.objects.get(id=access_token["user_id"])
                request.user = user
            except Exception as e:
                logger.error(f"JWT ошибка: {e}")

class JWTAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()

        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        scope["user"] = AnonymousUser()

        if token:
            try:
                access_token = AccessToken(token)
                User = get_user_model()
                user = await User.objects.aget(id=access_token["user_id"])
                scope["user"] = user
            except Exception as e:
                logger.error(f"JWT ошибка: {e}")
        return await self.inner(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))