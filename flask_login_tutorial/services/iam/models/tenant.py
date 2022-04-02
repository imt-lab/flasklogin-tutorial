from .... import db


class Tenant(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))

    def __init__(self, id=None, uuid=None, name=None, description=None):
        self.id = id
        self.uuid = uuid
        self.name = name
        self.description = description
