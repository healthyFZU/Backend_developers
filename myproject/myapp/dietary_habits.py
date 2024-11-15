from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

dietary_habits_blueprint = Blueprint('dietary_habits', __name__)

mysql = MySQL()

# 创建用户饮食习惯信息 API
@dietary_habits_blueprint.route('/user/<string:userId>/dietary-habits', methods=['POST'])
def create_user_dietary_habits(userId):
    data = request.get_json()
    # 从请求中获取饮食习惯数据
    diet_goals = data.get('diet_goals')
    taste_preference = data.get('taste_preference')
    avoid_certain_food = data.get('avoid_certain_food')
    fitness_planning = data.get('fitness_planning')
    exercise_habits = data.get('exercise_habits')

    # 检查必填字段
    if not all([diet_goals, taste_preference, avoid_certain_food, fitness_planning, exercise_habits]):
        return jsonify({'message': 'All fields are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    # 插入新的饮食习惯信息记录
    cur.execute("INSERT INTO user_dietary_habits (userId, diet_goals, taste_preference, avoid_certain_food, fitness_planning, exercise_habits) VALUES (%s, %s, %s, %s, %s, %s)",
                (userId, diet_goals, taste_preference, avoid_certain_food, fitness_planning, exercise_habits))
    mysql.connection.commit()
    new_dietary_habits_id = cur.lastrowid  # 获取新创建记录的ID
    cur.close()

    return jsonify({'message': '用户饮食习惯信息创建成功'}), 201

# 获取用户饮食习惯信息 API
@dietary_habits_blueprint.route('/user/<string:userId>/dietary-habits', methods=['GET'])
def get_user_dietary_habits(userId):
    cur = mysql.connection.cursor()

    # 查询用户饮食习惯信息记录
    cur.execute("SELECT * FROM user_dietary_habits WHERE userId = %s", (userId,))
    dietary_habits = cur.fetchone()
    cur.close()

    if dietary_habits:
        return jsonify({
            'userId': dietary_habits[0],
            'diet_goals': dietary_habits[1],
            'taste_preference': dietary_habits[2],
            'avoid_certain_food': dietary_habits[3],
            'fitness_planning': dietary_habits[4],
            'exercise_habits': dietary_habits[5],
            'created_at': dietary_habits[6],
            'updated_at': dietary_habits[7]
        }), 200
    else:
        return jsonify({'message': '用户饮食习惯信息不存在'}), 404

# 更新用户饮食习惯信息 API
@dietary_habits_blueprint.route('/user/<string:userId>/dietary-habit', methods=['PUT'])
def update_user_dietary_habits(userId):
    data = request.get_json()
    diet_goals = data.get('diet_goals')
    taste_preference = data.get('taste_preference')
    avoid_certain_food = data.get('avoid_certain_food')
    fitness_planning = data.get('fitness_planning')
    exercise_habits = data.get('exercise_habits')
    updated_at = datetime.now()

    # 连接数据库
    cur = mysql.connection.cursor()

    # 构建更新语句，仅更新用户提供的信息
    updates = []
    params = []

    if diet_goals:
        updates.append("diet_goals = %s")
        params.append(diet_goals)
    if taste_preference:
        updates.append("taste_preference = %s")
        params.append(taste_preference)
    if avoid_certain_food:
        updates.append("avoid_certain_food = %s")
        params.append(avoid_certain_food)
    if fitness_planning:
        updates.append("fitness_planning = %s")
        params.append(fitness_planning)
    if exercise_habits:
        updates.append("exercise_habits = %s")
        params.append(exercise_habits)
    updates.append("updated_at = %s")
    params.append(updated_at)

    # 如果没有要更新的信息，返回错误
    if not updates:
        return jsonify({'message': 'No update information provided!'}), 400

    # 更新用户饮食习惯信息记录
    params.append(userId)
    cur.execute("UPDATE user_dietary_habits SET " + ", ".join(updates) + " WHERE userId = %s", tuple(params))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Dietary habits not found or not updated!'}), 404
    else:
        return jsonify({'message': 'Dietary habits updated successfully!'}), 200

# 删除用户饮食习惯信息 API
@dietary_habits_blueprint.route('/user/<string:userId>/dietary-habit', methods=['DELETE'])
def delete_user_dietary_habits(userId):
    cur = mysql.connection.cursor()

    # 删除用户饮食习惯信息记录
    cur.execute("DELETE FROM user_dietary_habits WHERE userId = %s", (userId))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Dietary habits not found!'}), 404
    else:
        return jsonify({'message': 'Dietary habits deleted successfully!'}), 200