from ... import db

class GroupUser(db.Model):

    __tablename__ = 'group_user'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, 
                         db.ForeignKey('group.id'),
                         nullable=False)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('user.id'),
                        nullable=False)

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id

    def __repr__(self):
        return '<Group_User {0} {1}>'.format(self.group_id, self.user_id)