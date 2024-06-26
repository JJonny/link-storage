import os

import jwt

from datetime import datetime, timezone, timedelta

from starlette import status
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import config
from models.permission_role import PermissionRole
from utils.user_constants import ACTION, USER_ROLES, ALLOWED_USER_ROLES_SUBSCRIBER_ACCESS, ACCESS_TOKEN_TTL


### DEBUG only
def create_token() -> bytes:
    from utils.user_constants import PERMISSIONS
    payload = {}
    now = datetime.now(timezone.utc)
    expire = datetime.timestamp(now + timedelta(hours=ACCESS_TOKEN_TTL))
    payload["type"] = "access"
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = "123-456"
    payload["perms"] = [{USER_ROLES.admin: PERMISSIONS.admin_permissions}]

    return jwt.encode(payload, config.JWT_SECRET)


async def decode_jwt(token: str) -> dict:
    if int(os.getenv('DEBUG')):
        token = create_token()
    try:
        decoded_token = jwt.decode(token, config.JWT_SECRET, algorithms=['HS256'])
        if decoded_token['type'] == 'access':
            expiration_time = datetime.utcfromtimestamp(decoded_token["exp"])
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(hours=ACCESS_TOKEN_TTL))
            if datetime.timestamp(expiration_time) < target_timestamp:
                return decoded_token
    except Exception as e:
        raise e


class JWTBearer(HTTPBearer):
    """
    Class that persist authentication on routes.

    If the credential scheme isn't a bearer scheme, raised an exception for an invalid token scheme.
    If a bearer token was passed, verified that the JWT is valid.
    If no credentials were received, raised an invalid authorization error.
    """
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
            if not await self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")

    async def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = await decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


async def get_permissions(action: str, token: str) -> bool:
    """
    Check permissions from jwt token.

    A user can have multiple roles.
    Check a role for access to a specific content.
    Raise 403 exception iif has no access.
    """
    try:
        payload = await decode_jwt(token)
        user_permissions = []
        for user_perms in payload.get('perms'):
            user_permissions.extend([PermissionRole(name=role, permissions=perm) for role, perm in user_perms.items()])

        for permission_role in user_permissions:
            if action in ACTION.actions():
                if permission_role.name in USER_ROLES.get_constant_values():
                    return True
                else:
                    continue
            if action in ACTION.actions():
                if permission_role.name in ALLOWED_USER_ROLES_SUBSCRIBER_ACCESS:
                    return True
                else:
                    continue
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please register or buy subscription to get access to content."
        )
