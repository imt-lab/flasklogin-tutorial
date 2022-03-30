from ... import db


class GroupRole(db.Model):

    __tablename__ = 'group_role'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, nullable=False)

    def __init__(self, group_id, role_id):
        self.group_id = group_id
        self.role_id = role_id

    def __repr__(self):
        return '<Group_Role {0} {1}>'.format(self.group_id, self.role_id)
