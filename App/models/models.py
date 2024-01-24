from ..exts import db

# 模型就是类
# 继承db.model才是模型不然就是简单的类

class CategoryModel(db.Model):
    # table name 
    __tablename__ = 'tb_category'
    # filed 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(30), unique = True)
    describe = db.Column(db.String(255), default = 'describe')
    articles = db.relationship('ArticalModel', backref = 'category', lazy = 'dynamic')

class ArticalModel(db.Model):
    # table name 
    __tablename__ = 'tb_artical'
    # filed 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(30), unique = True)
    content = db.Column(db.Text(), default = 'content')
    keyWord = db.Column(db.String(255), default = 'key')
    img = db.Column(db.Text(), default = 'content')
    category_id = db.Column(db.Integer, db.ForeignKey(CategoryModel.id))

class PhotoModel(db.Model):
    __tablename__ = 'tb_photo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    url = db.Column(db.Text())
    name = db.Column(db.String(30), unique = True)
    describe = db.Column(db.Text(), default = 'describe')