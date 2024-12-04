from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

health_info_blueprint = Blueprint('health_info', __name__)

mysql = MySQL()

# 创建用户健康信息 API
# 创建用户健康信息 API
@health_info_blueprint.route('/user/<int:userId>/health-info', methods=['POST'])
def create_user_health_info(userId):
    data = request.get_json()
    # 从请求中获取健康信息数据
    blood_sugar = data.get('blood_sugar')
    blood_pressure = data.get('blood_pressure')
    allergens = data.get('allergens')
    recent_medications = data.get('recent_medications')
    past_medical_history = data.get('past_medical_history')
    other = data.get('other')  # 新增字段

    # 检查必填字段
    # if not all([blood_sugar, blood_pressure, allergens, recent_medications, past_medical_history]):
    #     return jsonify({'message': 'All fields are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    # 插入新的健康信息记录
    cur.execute("INSERT INTO user_health_info (userId, blood_sugar, blood_pressure, allergens, recent_medications, past_medical_history, other) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (userId, blood_sugar, blood_pressure, allergens, recent_medications, past_medical_history, other))
    mysql.connection.commit()
    new_health_info_id = cur.lastrowid  # 获取新创建记录的ID
    cur.close()

    return jsonify({'message': '用户健康信息创建成功', 'health_info_id': new_health_info_id}), 201


# 获取用户健康信息 API
@health_info_blueprint.route('/user/<int:userId>/health-infos', methods=['GET'])
def get_user_health_info(userId):
    cur = mysql.connection.cursor()

    # 查询用户健康信息记录
    cur.execute("SELECT * FROM user_health_info WHERE userId = %s", (userId,))
    health_info = cur.fetchone()
    cur.close()

    if health_info:
        return jsonify({
            'userId': health_info[0],
            'blood_sugar': health_info[1],
            'blood_pressure': health_info[2],
            'allergens': health_info[3],
            'recent_medications': health_info[4],
            'past_medical_history': health_info[5],
            'other':health_info[6],
            'created_at': health_info[7],
            'updated_at': health_info[8]
        }), 200
    else:
        return jsonify({'message': '用户健康信息不存在'}), 404

# 更新用户健康信息 API
@health_info_blueprint.route('/user/<int:userId>/health-info', methods=['PUT'])
def update_user_health_info(userId):
    data = request.get_json()
    blood_sugar = data.get('blood_sugar')
    blood_pressure = data.get('blood_pressure')
    allergens = data.get('allergens')
    recent_medications = data.get('recent_medications')
    past_medical_history = data.get('past_medical_history')
    other = data.get('other')
    updated_at = datetime.now()

    # 连接数据库
    cur = mysql.connection.cursor()

    # 构建更新语句，仅更新用户提供的信息
    updates = []
    params = []  # 先添加userId到params列表

    if blood_sugar:
        updates.append("blood_sugar = %s")
        params.append(blood_sugar)
    if blood_pressure:
        updates.append("blood_pressure = %s")
        params.append(blood_pressure)
    if allergens:
        updates.append("allergens = %s")
        params.append(allergens)
    if recent_medications:
        updates.append("recent_medications = %s")
        params.append(recent_medications)
    if past_medical_history:
        updates.append("past_medical_history = %s")
        params.append(past_medical_history)
    if other:
        updates.append("other = %s")
        params.append(other)
    updates.append("updated_at = %s")
    params.append(updated_at)

    # 如果没有要更新的信息，返回错误
    if not updates:
        return jsonify({'message': 'No update information provided!'}), 400
    params.append(userId)

    # 更新用户健康信息记录
    cur.execute("UPDATE user_health_info SET " + ", ".join(updates) + " WHERE userId = %s", tuple(params))

    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Health info not found or not updated!', 'data': data}), 404

    else:
        return jsonify({'message': 'Health info updated successfully!', 'data': data}), 200

# 删除用户健康信息 API
@health_info_blueprint.route('/user/<int:userId>/health-info', methods=['DELETE'])
def delete_user_health_info(userId):
    cur = mysql.connection.cursor()

    # 删除用户健康信息记录
    cur.execute("DELETE FROM user_health_info WHERE userId = %s", (userId,))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Health info not found!'}), 404
    else:
        return jsonify({'message': 'Health info deleted successfully!'}), 200
