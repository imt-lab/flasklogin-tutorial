"""Role Manager."""

from ...models.iam.role import Role


class RoleManager:
    
    def __init__(self):
        pass
    
    def create_new_role(self, role_name, description, tag):
        pass
    
    def get_role_by_name(self, role_name):
        pass
    
    def get_role_by_id(self, role_id):
        pass
    
    def list_roles(self):
        pass
    
    def delete_role_by_id(self, role_id):
        pass
    
    def delete_role_by_name(self, role_name):
        pass
    
    def update_role_by_id(self, role_id):
        pass
    
    def update_role_by_name(self, role_name):
        pass