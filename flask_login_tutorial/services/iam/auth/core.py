from functools import wraps
from os import abort

from flask import abort, request
from flask_login import login_user

from ..models.user import User


def api_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if "email" in request.headers and "api-key" in request.headers:
            email = request.headers["email"]
            api_key = request.headers["api-key"]
            user = User.query.filter_by(
                email=email, api_key=api_key, is_active=1, deleted=0
            ).first()
            if not user:
                abort(401)
            login_user(user)
        else:
            abort(400)

        return func(*args, **kwargs)

    return decorated_view
