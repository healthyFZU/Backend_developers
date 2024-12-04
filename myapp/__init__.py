from flask import Flask
from flask_cors import CORS
import os

# 从蓝图导入
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
from .recommend_questions import question_blueprint
from .file_upload import file_upload_blueprint
from .sports import sports_blueprint

from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    # 配置上传文件夹和允许的文件扩展名
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为 16MB

    # 确保上传目录存在
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # 配置数据库
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['MYSQL_HOST'] = '129.204.151.245'
    app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_USER'] = 'admin'
    app.config['MYSQL_PASSWORD'] = '@yangshiji123'
    app.config['MYSQL_DB'] = 'yangshiji_2'

    # 启用 CORS
    CORS(app)

    # 初始化数据库连接
    mysql = MySQL(app)

    # 初始化 bcrypt 和 JWT
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    # 注册所有蓝图
    app.register_blueprint(user_blueprint, url_prefix='/user')
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
    app.register_blueprint(question_blueprint)
    app.register_blueprint(file_upload_blueprint)  # 文件上传蓝图注册
    app.register_blueprint(sports_blueprint)
    return app
