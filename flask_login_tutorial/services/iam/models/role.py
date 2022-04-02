from .... import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    tag = db.Column(db.String(64))

    def __init__(self, id=None, name=None, description=None, tag=None):
        self.id = id
        self.name = name
        self.description = description
        self.tag = tag
