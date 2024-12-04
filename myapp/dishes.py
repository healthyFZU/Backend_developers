from flask import Flask, Blueprint, request, jsonify
from flask_mysqldb import MySQL
import json
import random
app = Flask(__name__)

# 配置数据库
mysql = MySQL(app)

# 创建菜品蓝图
dishes_blueprint = Blueprint('dishes', __name__)

# 创建菜品
@dishes_blueprint.route('/dishes', methods=['POST'])
def create_dish():
    data = request.get_json()  # 获取 JSON 格式的请求数据

    # 获取菜品信息
    dish_name = data.get('dish_name')
    ingredients = data.get('ingredients')
    nutrition = data.get('nutrition')
    types = data.get('types')  # 替换 'flavor' 为 'types'
    detail = data.get('detail')  # 替换 'flavor' 为 'detail'
    price = data.get('price')
    merchant_id = data.get('merchant_id')
    dish_image = data.get('dish_image')
    score = data.get('score')
    allergens = data.get('allergens')

    # 检查必填字段
    # if not all([dish_name, ingredients, nutrition, types, detail, price, merchant_id, dish_image, score, allergens]):
    #     return jsonify({'message': 'All fields are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    try:
        # 构造 SQL 查询，不包括 created_at 和 updated_at 字段，因为它们会自动生成
        query = """
        INSERT INTO dishes (dish_name, ingredients, nutrition, types, detail, price, merchant_id, dish_image, score, allergens)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (dish_name, json.dumps(ingredients), json.dumps(nutrition), types, detail, price, merchant_id, dish_image, score, json.dumps(allergens)))

        mysql.connection.commit()
        new_dish_id = cur.lastrowid  # 获取新创建记录的 ID
        cur.close()

        return jsonify({"message": "菜品创建成功", "dish_id": new_dish_id}), 201
    except Exception as e:
        # 打印异常信息到服务器日志
        cur.close()
        return jsonify({"message": "An error occurred while creating the dish.", "error": str(e)}), 500

# 查询所有菜品
def safe_json_loads(value, default=None):
    """
    安全解析 JSON 数据
    :param value: 数据库中存储的 JSON 字符串
    :param default: 默认值，当解析失败时返回
    :return: 解析后的 JSON 数据或默认值
    """
    try:
        return json.loads(value) if value else default
    except (TypeError, json.JSONDecodeError):
        print(f"Invalid JSON: {value}")  # 打印错误日志便于调试
        return default

@dishes_blueprint.route('/dishes', methods=['GET'])
def get_dishes():
    cur = mysql.connection.cursor()

    # 执行 SQL 查询
    query = "SELECT * FROM dishes"
    cur.execute(query)
    dishes = cur.fetchall()
    cur.close()

    # 将数据库结果转为 JSON 格式
    dishes_list = []
    for dish in dishes:
        dishes_list.append({
            "dishId": dish[0],                           # 菜品 ID
            "dish_name": dish[1],                        # 菜品名称
            "ingredients": safe_json_loads(dish[2], []), # 食材信息（解析为列表）
            "nutrition": safe_json_loads(dish[3], []),   # 营养成分（解析为列表）
            "types": dish[4] if dish[4] else "未知类型",  # 类型（默认值：未知类型）
            "introduction": dish[5] if dish[5] else "暂无介绍", # 简介（默认值：暂无介绍）
            "price": float(dish[6]) if dish[6] else 0.0, # 价格（默认值：0.0）
            "dish_image":dish[8],
            "merchant_id":dish[7],
	    "score":dish[9]
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
        try:
            # 解析 ingredients
            ingredients = json.loads(dish_info[2]) if dish_info[2] else []
        except json.JSONDecodeError:
            ingredients = []

        try:
            # 解析 nutrition
            if dish_info[3]:
                # 尝试用 JSON 解析 nutrition
                nutrition = json.loads(dish_info[3])
            else:
                nutrition = []
        except json.JSONDecodeError:
            # 如果 nutrition 是普通字符串，尝试用逗号分隔解析
            nutrition = dish_info[3].strip('"').split(",") if dish_info[3] else []

        # 确保 nutrition 是清洁的列表
        nutrition = [item.strip().strip('"').strip("'") for item in nutrition if item.strip()]

        try:
            # 解析 allergens
            allergens = json.loads(dish_info[10]) if dish_info[10] else []
        except json.JSONDecodeError:
            allergens = []

        # 返回 JSON 响应
        return jsonify({
            "dishId": dish_info[0],
            "dish_name": dish_info[1],
            "ingredients": ingredients,
            "nutrition": nutrition,
            "types": dish_info[4],
            "detail": dish_info[5],
            "price": dish_info[6],
            "merchant_id": dish_info[7],
            "dish_image": dish_info[8],
            "score": dish_info[9],
            "allergens": allergens
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
        params.append(json.dumps(data['ingredients']))
    if 'nutrition' in data:
        updates.append("nutrition = %s")
        params.append(json.dumps(data['nutrition']))
    if 'types' in data:
        updates.append("types = %s")
        params.append(data['types'])
    if 'detail' in data:
        updates.append("detail = %s")
        params.append(data['detail'])
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
        params.append(json.dumps(data['allergens']))

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

# 获取随机三个菜品
@dishes_blueprint.route('/dishes/random3', methods=['GET'])
def get_random_dishes():
    cur = mysql.connection.cursor()

    try:
        # 查询所有菜品的 ID
        cur.execute("SELECT dishId FROM dishes")
        dish_ids = [row[0] for row in cur.fetchall()]

        # 随机选择三个 ID
        random_ids = random.sample(dish_ids, min(3, len(dish_ids)))

        # 根据随机 ID 查询对应的菜品
        placeholders = ', '.join(['%s'] * len(random_ids))
        query = f"SELECT dishId, dish_name, dish_image, score, merchant_id FROM dishes WHERE dishId IN ({placeholders})"
        cur.execute(query, random_ids)
        dishes = cur.fetchall()

        # 关闭游标
        cur.close()

        # 将查询结果转换为 JSON 格式
        result = [
            {
                "dishId": dish[0],
                "dish_name": dish[1],
                "dish_image": dish[2],
                "score": dish[3],
                "merchant_id":dish[4]
            }
            for dish in dishes
        ]
        return jsonify(result), 200
    except Exception as e:
        cur.close()
        return jsonify({"message": "Error fetching random dishes", "error": str(e)}), 500

# 获取随机六个菜品
@dishes_blueprint.route('/dishes/random6', methods=['GET'])
def get_random_dishes_6():
    cur = mysql.connection.cursor()

    try:
        # 查询所有菜品的 ID
        cur.execute("SELECT dishId FROM dishes")
        dish_ids = [row[0] for row in cur.fetchall()]

        # 随机选择六个 ID
        random_ids = random.sample(dish_ids, min(6, len(dish_ids)))

        # 根据随机 ID 查询对应的菜品
        placeholders = ', '.join(['%s'] * len(random_ids))
        query = f"SELECT dishId, dish_name, dish_image, introduction, score, merchant_id FROM dishes WHERE dishId IN ({placeholders})"
        cur.execute(query, random_ids)
        dishes = cur.fetchall()

        # 关闭游标
        cur.close()

        # 将查询结果转换为 JSON 格式
        result = [
            {
                "dishId": dish[0],
                "dish_name": dish[1],
                "dish_image": dish[2],
                "introduction":dish[3],
                "score": dish[4],
                "merchant_id": dish[5]
            }
            for dish in dishes
        ]
        return jsonify(result), 200
    except Exception as e:
        cur.close()
        return jsonify({"message": "Error fetching random dishes", "error": str(e)}), 500
