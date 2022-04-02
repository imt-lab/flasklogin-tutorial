from functools import wraps
from flask_login import current_user
from flask import current_app


def admin_tenant_required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        print(current_user.level)
        if current_user.level not in [1, 2]:
            # return current_app.login_manager.unauthorized()
            print('you not allow this action')
        return func(*args, **kwargs)
    return decorated_view


def super_admin_required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.level == 2:
            print('you not allow this action')
        return func(*args, **kwargs)
    return decorated_view


class UserManager:

    def __init__(self):
        pass

    @admin_tenant_required
    def add_user(self):
        pass

    @admin_tenant_required
    def del_user(self):
        pass

    @admin_tenant_required
    def disable_user(self):
        pass

    @admin_tenant_required
    def enable_user(self):
        pass

    def get_user(self):
        pass

    @admin_tenant_required
    def update_otp(self):
        pass

    @admin_tenant_required
    def list_users(self):
        pass

    def change_password(self):
        pass


class GroupManager:

    def __init__(self):
        pass


class RoleManager:

    def __init__(self):
        pass


class TenantManager:

    def __init__(self):
        pass

    @super_admin_required
    def add_tenant(self):
        pass

    @super_admin_required
    def del_tenant(self):
        pass

    @super_admin_required
    def disable_tenant(self):
        pass

    @super_admin_required
    def update_tenant(self):
        pass

    @super_admin_required
    def assign_group_to_tenant(self):
        pass


class GroupRoleManager:

    def __init__(self):
        pass

    @admin_tenant_required
    def assign_role_to_group(self, role_id, group_id):
        pass

    @admin_tenant_required
    def unassign_role_to_group(self, role_id, group_id):
        pass


class GroupUserManager:

    def __init__(self):
        pass

    @admin_tenant_required
    def assign_user_to_group(self, user_id, group_id):
        pass

    @admin_tenant_required
    def unassign_user_to_group(self, user_id, group_id):
        pass
