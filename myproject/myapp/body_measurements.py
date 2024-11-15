from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

body_measurements_blueprint = Blueprint('body_measurements', __name__)

mysql = MySQL()

# 创建用户身体测量信息 API
@body_measurements_blueprint.route('/user/<string:userId>/measurements', methods=['POST'])
def create_user_measurements(userId):
    data = request.get_json()
    # 从请求中获取身体测量数据
    waist = data.get('waist')
    thigh = data.get('thigh')
    calf = data.get('calf')
    bust = data.get('bust')
    hips = data.get('hips')
    arm = data.get('arm')
    created_at = datetime.now()
    updated_at = created_at

    # 检查必填字段
    if not all([waist, thigh, calf, bust, hips, arm]):
        return jsonify({'message': 'All fields are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    # 插入新的身体测量信息记录
    cur.execute("INSERT INTO body_measurements (userId, waist, thigh, calf, bust, hips, arm, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (userId, waist, thigh, calf, bust, hips, arm, created_at, updated_at))
    mysql.connection.commit()
    new_measurement_id = cur.lastrowid  # 获取新创建记录的ID
    cur.close()

    return jsonify({'message': '用户身体测量信息创建成功', 'measurement_id': new_measurement_id}), 201

# 获取用户身体测量信息 API
@body_measurements_blueprint.route('/user/<string:userId>/measurements', methods=['GET'])
def get_user_measurements(userId):
    cur = mysql.connection.cursor()

    # 查询用户身体测量信息记录
    cur.execute("SELECT * FROM body_measurements WHERE userId = %s", (userId,))
    measurements = cur.fetchall()
    cur.close()

    if not measurements:
        return jsonify({'message': 'No measurements found!'}), 404

    # 返回身体测量信息
    measurement_data = []
    for measurement in measurements:
        measurement_data.append({
            'measurement_id': measurement[0],
            'userId': measurement[1],
            'waist': measurement[2],
            'thigh': measurement[3],
            'calf': measurement[4],
            'bust': measurement[5],
            'hips': measurement[6],
            'arm': measurement[7],
            'created_at': measurement[8],
            'updated_at': measurement[9]
        })

    return jsonify(measurement_data), 200

# 更新用户身体测量信息 API
@body_measurements_blueprint.route('/user/<string:userId>/measurements/<int:measurement_id>', methods=['PUT'])
def update_user_measurements(userId, measurement_id):
    data = request.get_json()
    waist = data.get('waist')
    thigh = data.get('thigh')
    calf = data.get('calf')
    bust = data.get('bust')
    hips = data.get('hips')
    arm = data.get('arm')
    updated_at = datetime.now()

    # 连接数据库
    cur = mysql.connection.cursor()

    # 构建更新语句，仅更新用户提供的信息
    updates = []
    params = []

    if waist:
        updates.append("waist = %s")
        params.append(waist)
    if thigh:
        updates.append("thigh = %s")
        params.append(thigh)
    if calf:
        updates.append("calf = %s")
        params.append(calf)
    if bust:
        updates.append("bust = %s")
        params.append(bust)
    if hips:
        updates.append("hips = %s")
        params.append(hips)
    if arm:
        updates.append("arm = %s")
        params.append(arm)
    updates.append("updated_at = %s")
    params.append(updated_at)

    # 如果没有要更新的信息，返回错误
    if not updates:
        return jsonify({'message': 'No update information provided!'}), 400

    # 更新用户身体测量信息记录
    params.append(userId)
    params.append(measurement_id)  # 添加userId和measurement_id作为查询条件
    cur.execute("UPDATE body_measurements SET " + ", ".join(updates) + " WHERE userId = %s AND measurement_id = %s", tuple(params))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Measurements not found or not updated!'}), 404
    else:
        return jsonify({'message': 'Measurements updated successfully!'}), 200

# 删除用户身体测量信息 API
@body_measurements_blueprint.route('/user/<string:userId>/measurements/<int:measurement_id>', methods=['DELETE'])
def delete_user_measurements(userId, measurement_id):
    cur = mysql.connection.cursor()

    # 删除用户身体测量信息记录
    cur.execute("DELETE FROM body_measurements WHERE userId = %s AND measurement_id = %s", (userId, measurement_id))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Measurements not found!'}), 404
    else:
        return jsonify({'message': 'Measurements deleted successfully!'}), 200