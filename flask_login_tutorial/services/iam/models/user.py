from .... import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import pyotp

class User(UserMixin, db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(
        db.String(200), primary_key=False, unique=False, nullable=True
    )
    level = db.Column(db.SmallInteger, nullable=False, default=0)
    login_type = db.Column(db.String(40), unique=False, nullable=False, default='local')
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    otp_secret = db.Column(db.String(16))
    confirmed = db.Column(db.SmallInteger, nullable=False, default=0)
    is_active = db.Column(db.SmallInteger, nullable=False, default=0)   # 0 - deactive; 1 - active
    deleted = db.Column(db.SmallInteger, nullable=False, default=0)     # 0 - existing, 1 - deleted
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'))
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)


    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def get_totp_uri(self):
        return "otpauth://totp/PowerDNS-Admin:{0}?secret={1}&issuer=PowerDNS-Admin".format(
            self.username, self.otp_secret)

    def verify_totp(self, token):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    
    def get_user_info_by_id(self):
        """Get user info by id"""
        user_info = User.query.get(int(self.id))
        return user_info

    def get_user_info_by_username(self):
        """Get user info by username"""
        user_info = User.query.filter(User.username == self.username).first()
        return user_info