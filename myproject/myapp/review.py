# myapp/review.py
from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

review_blueprint = Blueprint('review', __name__)

mysql = MySQL()

# 用户评价 API
@review_blueprint.route('/user/<int:userId>/review', methods=['POST'])
def create_user_review(userId):
    data = request.get_json()
    score = data.get('score')
    dish_id = data.get('dish_id')
    review = data.get('review')

    # 检查必填字段
    if not score or not dish_id or not review:
        return jsonify({'message': 'Score, dish_id, and review are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    # 插入新的用户评价记录
    cur.execute("INSERT INTO user_reviews (userId, dish_id, score, review) VALUES (%s, %s, %s, %s)",
                (userId, dish_id, score, review))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Review created successfully!'}), 201

# 查询用户评价记录 API
@review_blueprint.route('/user/<int:userId>/review/<int:reviewId>', methods=['GET'])
def get_user_review(userId, reviewId):
    cur = mysql.connection.cursor()

    # 查询用户评价记录
    cur.execute("SELECT * FROM user_reviews WHERE userId = %s AND review_id = %s",
                (userId, reviewId))
    review = cur.fetchone()
    cur.close()

    if review:
        return jsonify({
            'review_id': review[0],
            'userId': review[1],
            'dish_id': review[2],
            'score': review[3],
            'review': review[4],
            'created_at': review[5],
            'updated_at': review[6]
        }), 200
    else:
        return jsonify({'message': 'Review not found!'}), 404

# 更新用户评价记录 API
@review_blueprint.route('/user/<int:userId>/review/<int:reviewId>', methods=['PUT'])
def update_user_review(userId, reviewId):
    data = request.get_json()

    # 连接数据库
    cur = mysql.connection.cursor()

    # 构建更新语句，仅更新用户提供的信息
    updates = []
    params = []

    if 'score' in data:
        updates.append("score = %s")
        params.append(data['score'])
    if 'dish_id' in data:
        updates.append("dish_id = %s")
        params.append(data['dish_id'])
    if 'review' in data:
        updates.append("review = %s")
        params.append(data['review'])
    # 如果没有要更新的信息，返回错误
    if not updates:
        return jsonify({'message': 'No update information provided!'}), 400
    # 更新用户评价记录
    params.extend([userId, reviewId])  # 添加userId和reviewId作为查询条件
    cur.execute("UPDATE user_reviews SET " + ", ".join(updates) + " WHERE userId = %s AND review_id = %s", tuple(params))
    mysql.connection.commit()
    cur.close()
    if cur.rowcount == 0:
        return jsonify({'message': 'Review not found or not updated!'}), 404
    else:
        return jsonify({'message': 'Review updated successfully!'}), 200

# 删除用户评价记录 API
@review_blueprint.route('/user/<int:userId>/review/<int:reviewId>', methods=['DELETE'])
def delete_user_review(userId, reviewId):
    cur = mysql.connection.cursor()

    # 删除用户评价记录
    cur.execute("DELETE FROM user_reviews WHERE userId = %s AND review_id = %s",
                (userId, reviewId))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Review not found!'}), 404
    else:
        return jsonify({'message': 'Review deleted successfully!'}), 200

# 查询菜品的所有评价 API
@review_blueprint.route('/dish/<int:dishId>/reviews', methods=['GET'])
def get_dish_reviews(dishId):
    cur = mysql.connection.cursor()

    # 查询菜品的所有评价
    cur.execute("SELECT * FROM user_reviews WHERE dish_id = %s", (dishId,))
    reviews = cur.fetchall()
    cur.close()

    if not reviews:
        return jsonify({'message': 'No reviews found!'}), 404

    return jsonify([
        {
            'review_id': review[0],
            'userId': review[1],
            'dish_id': review[2],
            'score': review[3],
            'review': review[4],
            'created_at': review[5],
            'updated_at': review[6]
        }
        for review in reviews
    ]), 200