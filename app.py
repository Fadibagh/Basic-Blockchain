from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


db = SQLAlchemy()
 

def create_app():
     app = Flask(__name__, template_folder='templates')
     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userStorage.db'

     db.init_app(app)

     from routes import register_routes 
     register_routes(app, db)

     migrate = Migrate(app, db)

     return app


#hash passwords and embed in url verification
# deply using aws