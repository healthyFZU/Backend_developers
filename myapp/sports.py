# myapp/sports.py
from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
import json
import MySQLdb.cursors  # 导入 DictCursor
sports_blueprint = Blueprint('sports', __name__)
from datetime import datetime, timedelta

mysql = MySQL()

'''def validate_sports_data(sports_data):
    """验证 sports_data 的格式和内容"""
    required_keys = ['name', 'calories']
    if not isinstance(sports_data, dict):
        return False, 'Sports data must be a JSON object.'
    for key in required_keys:
        if key not in sports_data:
            return False, f'Missing required field: {key}'
    if not isinstance(sports_data['calories'], (int, float)) or sports_data['calories'] <= 0:
        return False, 'Calories must be a positive number.'
    return True, None
'''
# 创建用户运动记录 API
@sports_blueprint.route('/user/<int:userId>/sports', methods=['POST'])
def create_user_sports(userId):
    data = request.get_json()

    # 获取运动数据，如果没有提供，则为空字典
    sports_data = data.get('sports', {})

    # 如果提供了运动数据，验证其格式
    if sports_data:
        if not isinstance(sports_data, dict):
            return jsonify({'message': 'Sports data must be a JSON object.'}), 400

        # 确保每项运动消耗的热量是正数
        for sport, calories in sports_data.items():
            if not isinstance(calories, (int, float)) or calories <= 0:
                return jsonify({'message': f'Invalid calories value for {sport}.'}), 400

        # 将运动数据转换为 JSON 字符串
        sport_name_json = json.dumps(sports_data)
        total_calories = sum(sports_data.values())
    else:
        sport_name_json = json.dumps({})
        total_calories = 0

    # 连接数据库
    cur = mysql.connection.cursor()

    # 插入新的运动记录
    cur.execute("""
        INSERT INTO sport_record (userId, sport_name, calories_burned, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (userId, sport_name_json, total_calories, datetime.now(), datetime.now()))

    mysql.connection.commit()
    new_measurement_id = cur.lastrowid  # 获取新创建记录的 ID
    cur.close()

    return jsonify({'measurement_id': new_measurement_id, 'message': '运动记录创建成功!'}), 201


# 获取用户运动记录 API
@sports_blueprint.route('/user/<int:userId>/sports', methods=['GET'])
def get_user_sports(userId):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # 获取日期参数，如果没有传入则使用当天日期
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    print(f"接收到的日期参数: {date_str}")

    # 获取当天日期的开始和结束时间
    start_date = datetime.strptime(date_str, '%Y-%m-%d')
    end_date = start_date + timedelta(days=1)

    # 查询指定日期的运动总热量
    cur.execute(
        """
        SELECT SUM(calories_burned) AS total_calories
        FROM sport_record
        WHERE userId = %s AND created_at >= %s AND created_at < %s
        """,
        (userId, start_date, end_date)
    )
    result = cur.fetchone()
    total_calories = result['total_calories'] or 0  # 如果没有记录，则总热量为 0

    # 查询详细运动记录
    cur.execute(
        """
        SELECT measurement_id, userId, sport_name, created_at, updated_at, calories_burned
        FROM sport_record
        WHERE userId = %s AND created_at >= %s AND created_at < %s
        """,
        (userId, start_date, end_date)
    )
    sports_info = cur.fetchall()
    cur.close()

    if not sports_info:
        return jsonify({'message': 'No sports records found!', 'total_calories': total_calories}), 404

    sports_data = []
    for record in sports_info:
        # 将运动数据从 JSON 字符串转换回字典
        sport_name_dict = json.loads(record['sport_name'])
        sports_data.append({
            'measurement_id': record['measurement_id'],
            'userId': record['userId'],
            'sport_name': sport_name_dict,
            'created_at': record['created_at'].isoformat(),
            'updated_at': record['updated_at'].isoformat(),
            'calories': record['calories_burned']
        })

    return jsonify({'sports': sports_data, 'total_calories': total_calories}), 200


# 更新用户运动记录 API
@sports_blueprint.route('/user/<int:userId>/sports/<int:measurement_id>', methods=['PUT'])
def update_user_sports(userId, measurement_id):
    data = request.get_json()

    # 获取新的运动数据
    sports_data = data.get('sports')  # sports 是一个字典，如 {"跑步": 100, "游泳": 50}

    if not sports_data:
        return jsonify({'message': 'Sports data is required!'}), 400

    # 检查运动数据的格式
    if not isinstance(sports_data, dict):
        return jsonify({'message': 'Sports data must be a JSON object.'}), 400

    # 确保每项运动消耗的热量是正数
    for sport, calories in sports_data.items():
        if not isinstance(calories, (int, float)) or calories <= 0:
            return jsonify({'message': f'Invalid calories value for {sport}.'}), 400

    # 将运动数据转换为 JSON 字符串
    sport_name_json = json.dumps(sports_data)

    # 连接数据库
    cur = mysql.connection.cursor()

    # 更新运动记录
    cur.execute("""
        UPDATE sport_record 
        SET sport_name = %s, calories_burned = %s, updated_at = %s 
        WHERE userId = %s AND measurement_id = %s
    """, (sport_name_json, sum(sports_data.values()), datetime.now(), userId, measurement_id))
    mysql.connection.commit()

    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Sports record not found or not updated!'}), 404
    else:
        return jsonify({'message': 'Sports record updated successfully!'}), 200


# 删除用户运动记录 API
@sports_blueprint.route('/user/<int:userId>/sports/<int:measurement_id>', methods=['DELETE'])
def delete_user_sports(userId, measurement_id):
    cur = mysql.connection.cursor()

    # 删除运动记录
    cur.execute("DELETE FROM sport_record WHERE userId = %s AND measurement_id = %s", (userId, measurement_id))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Sports record not found!'}), 404
    else:
        return jsonify({'message': 'Sports record deleted successfully!'}), 200