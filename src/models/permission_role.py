from pydantic import BaseModel


class PermissionRole(BaseModel):

    name: str
    permissions: dict
