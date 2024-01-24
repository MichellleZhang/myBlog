# manage extensions 

# import plug-ins 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# initialization 
db = SQLAlchemy()
migrate = Migrate()

# coupling with app object 
def init_exts(app):
    db.init_app(app = app)
    migrate.init_app(app = app, db = db)