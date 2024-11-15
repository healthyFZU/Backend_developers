from flask import Blueprint, request, jsonify
import json
from flask_mysqldb import MySQL
from datetime import datetime

body_blueprint = Blueprint('body', __name__)

mysql = MySQL()

# 用户身体信息 API
@body_blueprint.route('/user/<string:userId>/body-info', methods=['POST'])
def create_user_body_info(userId):
    data = request.get_json()
    # 从请求中获取身体信息数据
    age = data.get('age')
    sex = data.get('sex')
    height = data.get('height')
    weight = data.get('weight')
    weight_target = data.get('weight_target')
    target = data.get('target')
    stage = data.get('stage')
    pre_over_time = data.get('pre_over_time')
    created_at = datetime.now()
    updated_at = created_at

    # 检查必填字段
    if not all([age, sex, height, weight, weight_target, target, stage, pre_over_time]):
        return jsonify({'message': 'All fields are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    # 插入新的身体信息记录
    cur.execute("INSERT INTO user_body_info (userId, age, sex, height, weight, weight_target, created_at, updated_at, target, stage, pre_over_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (userId, age, sex, height, weight, weight_target, created_at, updated_at, target, stage, pre_over_time))
    mysql.connection.commit()
    new_body_info_id = cur.lastrowid  # 获取新创建记录的ID
    cur.close()

    return jsonify({'message': '用户身体信息创建成功', 'body_info_id': new_body_info_id}), 201

@body_blueprint.route('/user/<string:userId>/body-info', methods=['GET'])
def get_user_body_info(userId):
    cur = mysql.connection.cursor()

    # 查询用户身体信息记录
    cur.execute("SELECT * FROM user_body_info WHERE userId = %s", (userId,))
    body_info = cur.fetchone()
    cur.close()

    if body_info:
        return jsonify({
            'userId': body_info[0],
            'age': body_info[1],
            'sex': body_info[2],
            'height': body_info[3],
            'weight': body_info[4],
            'weight_target': body_info[5],
            'created_at': body_info[6],
            'updated_at': body_info[7],
            'target': body_info[8],
            'stage': body_info[9],
            'pre_over_time': body_info[10]
        }), 200
    else:
        return jsonify({'message': '用户身体信息不存在'}), 404

@body_blueprint.route('/user/<string:userId>/body-info', methods=['PUT'])
def update_user_body_info(userId):
    data = request.get_json()
    age = data.get('age')
    sex = data.get('sex')
    height = data.get('height')
    weight = data.get('weight')
    weight_target = data.get('weight_target')
    target = data.get('target')
    stage = data.get('stage')
    pre_over_time = data.get('pre_over_time')
    updated_at = datetime.now()

    # 连接数据库
    cur = mysql.connection.cursor()

    # 构建更新语句，仅更新用户提供的信息
    updates = []
    params = []

    if age:
        updates.append("age = %s")
        params.append(age)
    if sex:
        updates.append("sex = %s")
        params.append(sex)
    if height:
        updates.append("height = %s")
        params.append(height)
    if weight:
        updates.append("weight = %s")
        params.append(weight)
    if weight_target:
        updates.append("weight_target = %s")
        params.append(weight_target)
    if target:
        updates.append("target = %s")
        params.append(target)
    if stage:
        updates.append("stage = %s")
        params.append(stage)
    if pre_over_time:
        updates.append("pre_over_time = %s")
        params.append(pre_over_time)
    updates.append("updated_at = %s")
    params.append(updated_at)

    # 如果没有要更新的信息，返回错误
    if not updates:
        return jsonify({'message': 'No update information provided!'}), 400

    # 更新用户身体信息记录
    params.append(userId)  # 添加userId作为查询条件
    cur.execute("UPDATE user_body_info SET " + ", ".join(updates) + " WHERE userId = %s", tuple(params))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Body info not found or not updated!'}), 404
    else:
        return jsonify({'message': 'Body info updated successfully!'}), 200

@body_blueprint.route('/user/<string:userId>/body-info', methods=['DELETE'])
def delete_user_body_info(userId):
    cur = mysql.connection.cursor()

    # 删除用户身体信息记录
    cur.execute("DELETE FROM user_body_info WHERE userId = %s", (userId,))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Body info not found!'}), 404
    else:
        return jsonify({'message': 'Body info deleted successfully!'}), 200