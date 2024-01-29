import datetime
from flask import Flask
from .views.views import blog
from .views.views_admin import admin
from .exts import init_exts


def create_app():
    application = Flask(__name__)
    application.register_blueprint(blueprint=blog)
    application.register_blueprint(blueprint=admin)

    # database configuration 
    # db_uri = 'sqlite:///sqlite3.db' # sqlite 配置
    # db_uri = 'mysql+pymysql://root:root666666@localhost:3306/blogdb' # mysql 配置 example
    db_uri = 'mysql+pymysql://granted:root666666@blogdb.c5iqok0qmj8q.us-east-2.rds.amazonaws.com:3306/blogdb' # mysql 配置 example
    application.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize plug-in
    init_exts(app = application)
    
    return application