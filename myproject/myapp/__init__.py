# myapp/__init__.py
from flask import Flask
from flask_cors import CORS

from .dishes import dishes_blueprint
from .ingredients import ingredients_blueprint
from .merchants import merchants_blueprint

from .user import user_blueprint
from .log import log_blueprint
from .review import review_blueprint
from .dailyIntake import dailyIntake_blueprint

from .body import body_blueprint
from .body_measurements import body_measurements_blueprint
from .health_info import health_info_blueprint
from .dietary_habits import dietary_habits_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['MYSQL_HOST'] = '129.204.151.245'
    app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_USER'] = 'admin'
    app.config['MYSQL_PASSWORD'] = '@yangshiji123'
    app.config['MYSQL_DB'] = 'yangshiji'
    # 启用 CORS
    CORS(app)
    from flask_mysqldb import MySQL
    mysql = MySQL(app)

    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt(app)

    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)

    CORS(app)

    app.register_blueprint(user_blueprint, url_prefix='/user')  # 确保这里有
    app.register_blueprint(log_blueprint)
    app.register_blueprint(review_blueprint)

    app.register_blueprint(dailyIntake_blueprint)
    app.register_blueprint(merchants_blueprint)
    app.register_blueprint(dishes_blueprint)
    app.register_blueprint(ingredients_blueprint)

    app.register_blueprint(body_blueprint)
    app.register_blueprint(body_measurements_blueprint)
    app.register_blueprint(health_info_blueprint)
    app.register_blueprint(dietary_habits_blueprint)
    return app