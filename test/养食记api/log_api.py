from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import json
# 初始化应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# 设置 MySQL 数据库连接
app.config['MYSQL_HOST'] = '129.204.151.245'
app.config['MYSQL_PORT'] = 3306  # MySQL 数据库端口
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '@yangshiji123'  # 数据库密码
app.config['MYSQL_DB'] = 'yangshiji'  # 数据库名

# 初始化 MySQL、bcrypt 和 JWT
mysql = MySQL(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# 启用 CORS 解决跨域问题
CORS(app)
# 用户打卡 API
@app.route('/user/log', methods=['POST'])
@jwt_required()  # 确保用户已登录
def user_log():
    data = request.get_json()
    current_user = get_jwt_identity()  # 获取当前用户的 phoneNum

    # 从请求中获取打卡数据
    year = data.get('year')
    month = data.get('month')
    log_days = data.get('log_days')  # log_days 应该是一个 JSON 格式的数据

    # 检查必填字段
    if not year or not month or not log_days:
        return jsonify({'message': 'Year, month, and log days are required!'}), 400

    # 检查 log_days 是否是有效的 JSON 格式
    if not isinstance(log_days, dict):  # 如果你期望是字典格式
        return jsonify({'message': 'log_days must be a valid JSON object!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    # 查询是否已有打卡记录
    cur.execute("SELECT * FROM user_logs WHERE userId = (SELECT Id FROM user_info WHERE phoneNum = %s) AND year = %s AND month = %s",
                (current_user, year, month))
    existing_log = cur.fetchone()

    if existing_log:
        return jsonify({'message': 'You have already logged this month!'}), 400

    # 插入新的打卡记录，log_days 以 JSON 格式存储
    cur.execute("INSERT INTO user_logs (userId, year, month, log_days) VALUES ((SELECT Id FROM user_info WHERE phoneNum = %s), %s, %s, %s)",
                (current_user, year, month, json.dumps(log_days)))  # 将 log_days 转换为 JSON 字符串
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Log created successfully!'}), 201

# 查询用户打卡记录 API
@app.route('/user/logs', methods=['GET'])
@jwt_required()  # 确保用户已登录
def get_user_logs():
    current_user = get_jwt_identity()  # 获取当前用户的 phoneNum

    # 连接数据库
    cur = mysql.connection.cursor()

    # 查询当前用户的所有打卡记录
    cur.execute("SELECT * FROM user_logs WHERE userId = (SELECT Id FROM user_info WHERE phoneNum = %s)",
                (current_user,))
    logs = cur.fetchall()
    cur.close()

    if not logs:
        return jsonify({'message': 'No logs found!'}), 404

    # 返回打卡记录
    log_data = []
    for log in logs:
        # 解析 JSON 格式的 log_days
        log_data.append({
            'Log_id': log[0],
            'userId': log[1],
            'year': log[2],
            'month': log[3],
            'log_days': json.loads(log[4]),  # 将 JSON 字符串转为 Python 对象
            'CreatedAt': log[5],
            'UpdateAt': log[6]
        })

    return jsonify(log_data), 200

# 更新用户打卡记录 API
@app.route('/user/log/<int:log_id>', methods=['PUT'])
@jwt_required()  # 确保用户已登录
def update_user_log(log_id):
    current_user = get_jwt_identity()  # 获取当前用户的 phoneNum
    data = request.get_json()

    # 从请求中获取更新数据
    log_days = data.get('log_days')

    if not log_days:
        return jsonify({'message': 'Log days are required!'}), 400

    # 检查 log_days 是否是有效的 JSON 格式
    if not isinstance(log_days, dict):
        return jsonify({'message': 'log_days must be a valid JSON object!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    # 检查该记录是否属于当前用户
    cur.execute("SELECT * FROM user_logs WHERE Log_id = %s AND userId = (SELECT Id FROM user_info WHERE phoneNum = %s)",
                (log_id, current_user))
    log = cur.fetchone()

    if not log:
        return jsonify({'message': 'Log not found or does not belong to the current user!'}), 404

    # 更新打卡记录
    cur.execute("UPDATE user_logs SET log_days = %s WHERE Log_id = %s",
                (json.dumps(log_days), log_id))  # 将 log_days 转换为 JSON 字符串
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Log updated successfully!'}), 200

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
