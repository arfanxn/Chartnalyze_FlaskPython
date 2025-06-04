from enum import Enum

class PermissionName(Enum):
    ALL = '*'

    DASHBOARD_INDEX = 'dashboard.index'

    USERS_INDEX = 'users.index'
    USERS_SHOW = 'users.show'
    USERS_STORE = 'users.store'
    USERS_UPDATE = 'users.update'
    USERS_DESTROY = 'users.destroy'

    ROLES_INDEX = 'roles.index'
    ROLES_SHOW = 'roles.show'
    ROLES_STORE = 'roles.store'
    ROLES_UPDATE = 'roles.update'
    ROLES_DESTROY = 'roles.destroy'

    PERMISSIONS_INDEX = 'permissions.index'
    PERMISSIONS_SHOW = 'permissions.show'
    PERMISSIONS_STORE = 'permissions.store'
    PERMISSIONS_UPDATE = 'permissions.update'
    PERMISSIONS_DESTROY = 'permissions.destroy'

    POSTS_DESTROY = 'posts.destroy'

    COMMENTS_DESTROY = 'comments.destroy'
