from ..exts import db

class AdminUserModel(db.Model):
    __tablename__= 'tb_administration'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(30), unique = True)
    password = db.Column(db.Integer)