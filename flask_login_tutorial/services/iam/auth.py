
import uuid
from ... import db
from ...models.iam.user import User
from ...models.iam.tenant import Tenant
from ...models.iam.group import Group
from ...models.iam import USER_LEVEL_TENANT_ADMIN

def signup(username: str, email: str, password: str) -> str:
    """Signup

    Args:
        username (str): _description_
        email (str): _description_
        password (str): _description_
    """
    msg = ''
    existing_user = User.query.filter_by(username=username, 
                                         email=email,
                                         level=USER_LEVEL_TENANT_ADMIN,
                                         login_type='local', 
                                         deleted=0).first()
    if existing_user is None:
        try:
            # 1. Create new tenant 
            tenant_uuid = uuid.uuid4().hex
            tenant = Tenant(
                uuid=tenant_uuid,
                name='my-tenant {}'.format(tenant_uuid),
                description='Tenant\'s {}'.format(email)
            )
            db.session.add(tenant)
            
            # 2. Create new user with level: tenant admin
            user = User(
                username=username, 
                email=email, 
                level=USER_LEVEL_TENANT_ADMIN,
                local_type='local',
                tenant_uuid=tenant_uuid
            )
            user.set_password(password)
            db.session.add(user)
            
            # 3. Create new group: admin
            group = Group(
                name='admin',
                description='admin group',
                tenant_uuid=tenant_uuid
            )
            db.session.add(group)
            
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            msg = 'Create user error'
    else:
        msg = 'User existed'
    
    return msg