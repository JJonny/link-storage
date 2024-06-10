"""Users constants."""


class ConstantContainer(type):
    """Add some handy methods to container class."""

    def __new__(mcs, name, bases, attrs):
        """Attach method to class."""
        cls = super().__new__(mcs, name, bases, attrs)
        constant_values = []
        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith("__"):
                constant_values.append(attr_value)
        cls.get_constant_values = lambda: tuple(constant_values)
        return cls


ACCESS_TOKEN_TTL = 1  # one hour


class USER_ROLES(metaclass=ConstantContainer):

    admin = "ADMIN"
    superuser = "SUPERUSER"
    subscriber = "SUBSCRIBER"
    default = "USER"


class ACTION(metaclass=ConstantContainer):

    get_all_by_user = 'get_all_by_user'
    save_data = 'save_data'
    get_all_users = 'get_all_users'

    @staticmethod
    def actions() -> tuple[str]:
        return tuple(attr for attr in ACTION.__dict__ if not attr.startswith('__'))


class PERMISSIONS(metaclass=ConstantContainer):

    superuser_permissions = {
        'ALL_PERMISSION': {
            'read': True,
            'create': True,
            'update': True,
            'delete': True,
        }
    }

    subscriber_permissions = {
        'USERS': {
            'read': False,
            'create': False,
            'update': False,
            'delete': False,
        },
        'LINK_LIST': {
            'read': True,
            'create': True,
            'update': False,
            'delete': True,
        },
    }

    admin_permissions = {
        'USERS': {
            'create': True,
            'read': True,
            'update': True,
            'delete': True,
        },
        'LINK_LIST': {
            'read': True,
            'create': False,
            'update': False,
            'delete': True,
        },
    }


ALLOWED_USER_ROLES_SUBSCRIBER_ACCESS = (
    USER_ROLES.superuser,
    USER_ROLES.admin,
    USER_ROLES.subscriber,
)
