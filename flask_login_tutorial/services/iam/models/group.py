from .... import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id"))

    def __init__(self, id=None, name=None, description=None, tenant_id=None):
        self.id = id
        self.name = name
        self.description = description
        self.tenant_id = tenant_id
