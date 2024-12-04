# myapp/daily_intake.py
from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
import json

dailyIntake_blueprint = Blueprint('dailyIntake', __name__)

mysql = MySQL()

@dailyIntake_blueprint.route('/user/<int:userId>/intake', methods=['POST'])
def create_daily_intake(userId):
    data = request.get_json()
    date = data.get('date')
    eat_target = data.get('eat_target')
    breakfast = json.dumps(data.get('breakfast', []))
    lunch = json.dumps(data.get('lunch', []))
    dinner = json.dumps(data.get('dinner', []))
    more = json.dumps(data.get('more', []))
    have_eat = json.dumps(data.get('have_eat', []))
    drink_target = data.get('drink_target')
    have_drink = json.dumps(data.get('have_drink', []))
    sports= json.dumps(data.get('sports',[]))
    # 检查必填字段
    # if not all([date, eat_target, breakfast, lunch, dinner, more, have_eat, drink_target, have_drink]):
    #     return jsonify({'message': 'All fields are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    # 插入新的用户每日摄入记录
    cur.execute("""
        INSERT INTO daily_intake 
        (userId,date, eat_target, breakfast, lunch, dinner, more, have_eat, drink_target, have_drink,sports) 
        VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
    """,
                (userId,date, eat_target, breakfast, lunch, dinner, more, have_eat, drink_target, have_drink,sports))
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
        # 将JSON字符串转换回Python对象
        intake_data = {
            'intake_id': intake[0],
            'userId': intake[1],
            'date': intake[2],
            'eat_target': intake[3],
            'breakfast': json.loads(intake[4]),
            'lunch': json.loads(intake[5]),
            'dinner': json.loads(intake[6]),
            'more': json.loads(intake[7]),
            'have_eat': json.loads(intake[8]),
            'drink_target': intake[9],
            'have_drink': json.loads(intake[10]),
            'created_at': intake[11],
            'updated_at': intake[12],
            'sports':json.loads(intake[13])
        }
        return jsonify(intake_data), 200
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
    if 'eat_target' in data:
        updates.append("eat_target = %s")
        params.append(data['eat_target'])
    if 'breakfast' in data:
        updates.append("breakfast = %s")
        params.append(json.dumps(data['breakfast']))
    if 'lunch' in data:
        updates.append("lunch = %s")
        params.append(json.dumps(data['lunch']))
    if 'dinner' in data:
        updates.append("dinner = %s")
        params.append(json.dumps(data['dinner']))
    if 'more' in data:
        updates.append("more = %s")
        params.append(json.dumps(data['more']))
    if 'have_eat' in data:
        updates.append("have_eat = %s")
        params.append(json.dumps(data['have_eat']))
    if 'drink_target' in data:
        updates.append("drink_target = %s")
        params.append(data['drink_target'])
    if 'have_drink' in data:
        updates.append("have_drink = %s")
        params.append(json.dumps(data['have_drink']))
    if 'sports' in data:
        updates.append("sports = %s")
        params.append(json.dumps(data['sports']))
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
#根据用户id和日期查询表
@dailyIntake_blueprint.route('/user/<int:userId>/intake/date/<date>', methods=['GET'])
def get_daily_intake_by_date(userId, date):
    cur = mysql.connection.cursor()

    # 查询特定日期的用户每日摄入记录
    cur.execute("SELECT * FROM daily_intake WHERE userId = %s AND date = %s",
                (userId, date))
    intake = cur.fetchone()
    cur.close()

    if intake:
        # 将JSON字符串转换回Python对象
        intake_data = {
            'intake_id': intake[0],
            'userId': intake[1],
            'date': intake[2],
            'eat_target': intake[3],
            'breakfast': json.loads(intake[4]),
            'lunch': json.loads(intake[5]),
            'dinner': json.loads(intake[6]),
            'more': json.loads(intake[7]),
            'have_eat': json.loads(intake[8]),
            'drink_target': intake[9],
            'have_drink': json.loads(intake[10]),
            'created_at': intake[11],
            'updated_at': intake[12],
            'sports':json.loads(intake[13])
        }
        return jsonify(intake_data), 200
    else:
        return jsonify({'message': 'Daily intake not found for the given date!'}), 404
