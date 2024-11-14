# myapp/daily_intake.py
from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

dailyIntake_blueprint = Blueprint('dailyIntake', __name__)

mysql = MySQL()

@dailyIntake_blueprint.route('/user/<int:userId>/intake', methods=['POST'])
def create_daily_intake(userId):
    data = request.get_json()
    intake_date = data.get('intake_date')
    water_target = data.get('water_target')
    have_drunk = data.get('have_drunk')
    energy_target = data.get('energy_target')
    energy_consumed = data.get('energy_consumed')

    # 检查必填字段
    if not intake_date or not water_target or not have_drunk or not energy_target or not energy_consumed:
        return jsonify({'message': 'All fields are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    # 插入新的用户每日摄入记录
    cur.execute("INSERT INTO daily_intake (userId, intake_date, water_target, have_drunk, energy_target, energy_consumed) VALUES (%s, %s, %s, %s, %s, %s)",
                (userId, intake_date, water_target, have_drunk, energy_target, energy_consumed))
    mysql.connection.commit()
    new_intake_id = cur.lastrowid  # 获取新创建记录的ID
    cur.close()

    return jsonify({'intake_id': new_intake_id, 'message': 'Daily intake created successfully!'}), 201

@dailyIntake_blueprint.route('/user/<int:userId>/intake/<int:intakeId>', methods=['GET'])
def get_daily_intake(userId, intakeId):
    cur = mysql.connection.cursor()

    # 查询用户每日摄入记录
    cur.execute("SELECT * FROM daily_intake WHERE userId = %s AND intake_id = %s",
                (userId, intakeId))
    intake = cur.fetchone()
    cur.close()

    if intake:
        return jsonify({
            'intake_id': intake[0],
            'userId': intake[1],
            'intake_date': intake[2],
            'water_target': intake[3],
            'have_drunk': intake[4],
            'energy_target': intake[5],
            'energy_consumed': intake[6],
            'created_at': intake[7],
            'updated_at': intake[8]
        }), 200
    else:
        return jsonify({'message': 'Daily intake not found!'}), 404

@dailyIntake_blueprint.route('/user/<int:userId>/intake/<int:intakeId>', methods=['PUT'])
def update_daily_intake(userId, intakeId):
    data = request.get_json()

    # 连接数据库
    cur = mysql.connection.cursor()

    # 构建更新语句，仅更新用户提供的信息
    updates = []
    params = []

    if 'water_target' in data:
        updates.append("water_target = %s")
        params.append(data['water_target'])
    if 'have_drunk' in data:
        updates.append("have_drunk = %s")
        params.append(data['have_drunk'])
    if 'energy_target' in data:
        updates.append("energy_target = %s")
        params.append(data['energy_target'])
    if 'energy_consumed' in data:
        updates.append("energy_consumed = %s")
        params.append(data['energy_consumed'])

    # 如果没有要更新的信息，返回错误
    if not updates:
        return jsonify({'message': 'No update information provided!'}), 400

    # 更新用户每日摄入记录
    params.extend([userId, intakeId])  # 添加userId和intakeId作为查询条件
    cur.execute("UPDATE daily_intake SET " + ", ".join(updates) + " WHERE userId = %s AND intake_id = %s", tuple(params))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Daily intake not found or not updated!'}), 404
    else:
        return jsonify({'message': 'Daily intake updated successfully!'}), 200

@dailyIntake_blueprint.route('/user/<int:userId>/intake/<int:intakeId>', methods=['DELETE'])
def delete_daily_intake(userId, intakeId):
    cur = mysql.connection.cursor()

    # 删除用户每日摄入记录
    cur.execute("DELETE FROM daily_intake WHERE userId = %s AND intake_id = %s",
                (userId, intakeId))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Daily intake not found!'}), 404
    else:
        return jsonify({'message': 'Daily intake deleted successfully!'}), 200

@dailyIntake_blueprint.route('/user/<int:userId>/intake/date/<date>', methods=['GET'])
def get_daily_intake_by_date(userId, date):
    cur = mysql.connection.cursor()

    # 查询特定日期的用户每日摄入记录
    cur.execute("SELECT * FROM daily_intake WHERE userId = %s AND intake_date = %s",
                (userId, date))
    intake = cur.fetchone()
    cur.close()

    if intake:
        return jsonify({
            'intake_id': intake[0],
            'userId': intake[1],
            'intake_date': intake[2],
            'water_target': intake[3],
            'have_drunk': intake[4],
            'energy_target': intake[5],
            'energy_consumed': intake[6],
            'created_at': intake[7],
            'updated_at': intake[8]
        }), 200
    else:
        return jsonify({'message': 'Daily intake not found for the given date!'}), 404