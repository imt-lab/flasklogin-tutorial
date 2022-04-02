from flask_login import current_user, login_user

from .... import login_manager
from ..models.user import User


def login_local(email: str, password: str):

    user = User.query.filter_by(
        email=email, login_type="local", is_active=1, deleted=0
    ).first()
    if not user:
        return "user not exist or not active"
    if not user.check_password(password=password):
        return "password not correct"
    login_user(user)


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None
