from flask import Flask, Blueprint, request, jsonify
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

# 配置数据库
mysql = MySQL(app)

# 创建菜品蓝图
dishes_blueprint = Blueprint('dishes', __name__)

@dishes_blueprint.route('/dishes', methods=['POST'])
def create_dish():
    data = request.get_json()  # 获取 JSON 格式的请求数据

    # 获取菜品信息
    dish_name = data.get('dish_name')
    ingredients = data.get('ingredients')
    nutrition = data.get('nutrition')
    flavor = data.get('flavor')
    cuisine = data.get('cuisine')
    price = data.get('price')
    merchant_id = data.get('merchant_id')
    dish_image = data.get('dish_image')
    score = data.get('score')
    allergens = data.get('allergens')

    # 检查必填字段
    if not all([dish_name, ingredients, nutrition, flavor, cuisine, price, merchant_id, dish_image, score, allergens]):
        return jsonify({'message': 'All fields are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    try:
        # 构造 SQL 查询，不包括 created_at 和 updated_at 字段，因为它们会自动生成
        query = """
        INSERT INTO dishes (dish_name, ingredients, nutrition, flavor, cuisine, price, merchant_id, dish_image, score, allergens)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (dish_name, ingredients, nutrition, flavor, cuisine, price, merchant_id, dish_image, score, allergens))

        mysql.connection.commit()
        new_dish_id = cur.lastrowid  # 获取新创建记录的 ID
        cur.close()

        return jsonify({"message": "菜品创建成功", "dish_id": new_dish_id}), 201
    except Exception as e:
        # 打印异常信息到服务器日志
        cur.close()
        return jsonify({"message": "An error occurred while creating the dish.", "error": str(e)}), 500

# 查询所有菜品
@dishes_blueprint.route('/dishes', methods=['GET'])
def get_dishes():
    cur = mysql.connection.cursor()

    # 构造 SQL 查询
    query = "SELECT * FROM dishes"
    cur.execute(query)
    dishes = cur.fetchall()
    cur.close()

    dishes_list = []
    for dish in dishes:
        dishes_list.append({
            "dishId": dish[0],
            "dish_name": dish[1],
            "ingredients": dish[2],
            "nutrition": dish[3],
            "flavor": dish[4],
            "cuisine": dish[5],
            "price": dish[6],
            "merchant_id": dish[7],
            "dish_image": dish[8],
            "score": dish[9],
            "allergens": dish[10]
        })

    return jsonify(dishes_list), 200

# 查询单个菜品
@dishes_blueprint.route('/dishes/<int:dishId>', methods=['GET'])
def get_dish(dishId):
    cur = mysql.connection.cursor()

    # 构造 SQL 查询
    query = "SELECT * FROM dishes WHERE dishId = %s"
    cur.execute(query, (dishId,))
    dish_info = cur.fetchone()
    cur.close()

    if dish_info:
        return jsonify({
            "dishId": dish_info[0],
            "dish_name": dish_info[1],
            "ingredients": dish_info[2],
            "nutrition": dish_info[3],
            "flavor": dish_info[4],
            "cuisine": dish_info[5],
            "price": dish_info[6],
            "merchant_id": dish_info[7],
            "dish_image": dish_info[8],
            "score": dish_info[9],
            "allergens": dish_info[10]
        }), 200
    else:
        return jsonify({"message": "菜品不存在"}), 404

# 更新菜品
@dishes_blueprint.route('/dishes/<int:dishId>', methods=['PUT'])
def update_dish(dishId):
    data = request.get_json()  # 获取 JSON 格式的请求数据
    cur = mysql.connection.cursor()

    # 构建更新语句，仅更新用户提供的信息
    updates = []
    params = []

    if 'dish_name' in data:
        updates.append("dish_name = %s")
        params.append(data['dish_name'])
    if 'ingredients' in data:
        updates.append("ingredients = %s")
        params.append(data['ingredients'])
    if 'nutrition' in data:
        updates.append("nutrition = %s")
        params.append(data['nutrition'])
    if 'flavor' in data:
        updates.append("flavor = %s")
        params.append(data['flavor'])
    if 'cuisine' in data:
        updates.append("cuisine = %s")
        params.append(data['cuisine'])
    if 'price' in data:
        updates.append("price = %s")
        params.append(data['price'])
    if 'merchant_id' in data:
        updates.append("merchant_id = %s")
        params.append(data['merchant_id'])
    if 'dish_image' in data:
        updates.append("dish_image = %s")
        params.append(data['dish_image'])
    if 'score' in data:
        updates.append("score = %s")
        params.append(data['score'])
    if 'allergens' in data:
        updates.append("allergens = %s")
        params.append(data['allergens'])

    # 如果没有要更新的信息，返回错误
    if not updates:
        return jsonify({'message': 'No update information provided!'}), 400

    # 添加更新时间
    updates.append("updated_at = NOW()")
    params.append(dishId)  # 添加dishId作为查询条件

    # 构建完整的更新语句
    query = "UPDATE dishes SET " + ", ".join(updates) + " WHERE dishId = %s"
    cur.execute(query, tuple(params))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Dish not found or not updated!'}), 404
    else:
        return jsonify({'message': 'Dish updated successfully!'}), 200

# 删除菜品
@dishes_blueprint.route('/dishes/<int:dishId>', methods=['DELETE'])
def delete_dish(dishId):
    cur = mysql.connection.cursor()

    # 构造 SQL 查询
    query = "DELETE FROM dishes WHERE dishId = %s"
    cur.execute(query, (dishId,))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Dish not found!'}), 404
    else:
        return jsonify({'message': 'Dish deleted successfully!'}), 200



