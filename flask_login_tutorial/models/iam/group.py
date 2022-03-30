from ... import db

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(64))
    tenant_uuid = db.Column(db.String(64), nullable=False)
    
    def __init__(self, id=None, name=None, description=None, tenant_uuid=None):
        self.id = id
        self.name = name
        self.description = description
        self.tenant_uuid = tenant_uuid