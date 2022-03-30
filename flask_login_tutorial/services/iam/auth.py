
import uuid
from ... import db
from ...models.iam.user import User
from ...models.iam.tenant import Tenant
from ...models.iam.group import Group
from ...models.iam import USER_LEVEL_TENANT_ADMIN

def delete_tenant_by_id(id):
    """Delete tenant by id"""
    print("deleting...")
    User.query.filter_by(id=id).delete()
    db.session.commit()
    
def signup(username: str, email: str, password: str) -> str:
    """Signup"""
    
    msg = ''
    existing_user = User.query.filter_by(username=username, 
                                         email=email,
                                         level=USER_LEVEL_TENANT_ADMIN,
                                         login_type='local', 
                                         deleted=0).first()
    if existing_user is None:
        tenant_id = None
        try:
            # 1. Create new tenant 
            tenant_uuid = uuid.uuid4().hex
            tenant = Tenant(
                uuid=tenant_uuid,
                name='my-tenant {}'.format(tenant_uuid),
                description='Tenant\'s {}'.format(email)
            )
            db.session.add(tenant)
            db.session.commit()
            db.session.refresh(tenant)
            tenant_id = tenant.id
            
            # 2. Create new user with level: tenant admin
            user = User(
                username=username, 
                email=email, 
                level=USER_LEVEL_TENANT_ADMIN,
                logic_type='local',
                tenant_id=tenant_id
            )
            user.set_password(password)
            db.session.add(user)
            
            # 3. Create new group: admin
            group = Group(
                name='admin',
                description='admin group',
                tenant_id=tenant_id
            )
            db.session.add(group)
            
            db.session.commit()
            
        except Exception as e:
            print(e)
            db.session.rollback()
            msg = 'Create user error'
        if tenant_id:
            delete_tenant_by_id(tenant_id)
    else:
        msg = 'User existed'
    
    return msg