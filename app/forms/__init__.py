from wtforms import Form
from app.helpers.form_helpers import try_validate   

from .query_form import QueryForm

from .login_form import LoginForm
from .register_form import RegisterForm

from .update_user_form import UpdateUserForm
from .update_user_email_form import UpdateUserEmailForm
from .update_user_password_form import UpdateUserPasswordForm
from .reset_user_password_form import ResetUserPasswordForm

from .send_otp_form import SendOtpForm
from .otp_code_form import OtpCodeForm

from .assign_user_role import AssignUserRoleForm

from .store_watched_asset import StoreWatchedAssetForm
from .update_watched_asset_order import UpdateWatchedAssetOrderForm

from .save_post import SavePostForm

Form.try_validate = try_validate