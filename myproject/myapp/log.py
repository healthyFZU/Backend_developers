from flask import Blueprint, request, jsonify
import json
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

log_blueprint = Blueprint('log', __name__)

mysql = MySQL()
bcrypt = Bcrypt()
jwt = JWTManager()

# 用户打卡 API
@log_blueprint.route('/user/<int:userId>/log', methods=['POST'])
def user_log(userId):
    data = request.get_json()
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
    cur.execute("SELECT * FROM user_logs WHERE userId = %s AND year = %s AND month = %s",
                (userId, year, month))
    existing_log = cur.fetchone()

    if existing_log:
        return jsonify({'message': 'You have already logged this month!'}), 400

    # 插入新的打卡记录，log_days 以 JSON 格式存储
    cur.execute("INSERT INTO user_logs (userId, year, month, log_days) VALUES (%s, %s, %s, %s)",
                (userId, year, month, json.dumps(log_days)))  # 将 log_days 转换为 JSON 字符串
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Log created successfully!'}), 201

# 查询用户打卡记录 API
@log_blueprint.route('/user/<int:userId>/logs', methods=['GET'])
def get_user_logs(userId):
    # 连接数据库
    cur = mysql.connection.cursor()
    # 查询所有打卡记录
    cur.execute("SELECT * FROM user_logs WHERE userId = %s", (userId,))
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
            'UpdatedAt': log[6]  # Corrected the field name to match the standard
        })

    return jsonify(log_data), 200

# 更新用户打卡记录 API
@log_blueprint.route('/user/<int:userId>/log/<int:log_id>', methods=['PUT'])
def update_user_log(userId, log_id):
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

    # 更新打卡记录
    cur.execute("UPDATE user_logs SET log_days = %s WHERE userId = %s AND Log_id = %s",
                (json.dumps(log_days), userId, log_id))  # 将 log_days 转换为 JSON 字符串
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Log not found or not updated!'}), 404
    else:
        return jsonify({'message': 'Log updated successfully!'}), 200