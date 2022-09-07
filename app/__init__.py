from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_cors import CORS

# import blueprints
from .auth.routes import auth
from .ig.routes import ig
from .shop.routes import shop
from .shop2.routes import shop2
from .models import User

app = Flask(__name__)
login = LoginManager()
moment = Moment(app)
CORS(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# register blueprints
app.register_blueprint(auth)
app.register_blueprint(ig)
app.register_blueprint(shop)
app.register_blueprint(shop2)

app.config.from_object(Config)

# initialize database to work with our app
from .models import db

db.init_app(app)
migrate = Migrate(app, db)
login.init_app(app)


login.login_view = 'auth.logMeIn'


from . import routes
from . import models