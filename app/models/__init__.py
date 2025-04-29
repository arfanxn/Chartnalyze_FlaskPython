# Import association tables first
from .role_user import RoleUser
from .permission_role import PermissionRole

# Then import other models
from .user import User
from .role import Role
from .permission import Permission
from .otp import Otp