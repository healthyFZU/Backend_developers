from random import random

from flask import Flask, Blueprint, request, jsonify
from flask_mysqldb import MySQL
import json
from datetime import datetime
import random

app = Flask(__name__)

# 配置数据库
mysql = MySQL(app)

# 创建食材蓝图
ingredients_blueprint = Blueprint('ingredients', __name__)

@ingredients_blueprint.route('/ingredients', methods=['POST'])
def create_ingredient():
    data = request.get_json()  # 获取 JSON 格式的请求数据

    # 获取食材信息
    ingredient_name = data.get('ingredient_name')
    efficacy = data.get('efficacy')
    contraindications = data.get('contraindications')
    type_ = data.get('type')
    nutritions = data.get('nutritions')
    unit_heat = data.get('unit_heat')

    # 检查必填字段
    if not all([ingredient_name, type_]):
        return jsonify({'message': 'All fields are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    try:
        # 构造 SQL 查询，不包括 created_at 和 updated_at 字段，因为它们会自动生成
        query = """
        INSERT INTO ingredients (ingredient_name, efficacy, contraindications, type, nutritions, unit_heat)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (ingredient_name, efficacy, contraindications, type_, nutritions, unit_heat))

        mysql.connection.commit()
        new_ingredient_id = cur.lastrowid  # 获取新创建记录的 ID
        cur.close()

        return jsonify({"message": "食材创建成功", "ingredient_id": new_ingredient_id}), 201
    except Exception as e:
        # 打印异常信息到服务器日志
        cur.close()
        return jsonify({"message": "An error occurred while creating the ingredient.", "error": str(e)}), 500

# 查询所有食材
@ingredients_blueprint.route('/ingredients', methods=['GET'])
def get_ingredients():
    cur = mysql.connection.cursor()

    # 构造 SQL 查询
    query = "SELECT * FROM ingredients"
    cur.execute(query)
    ingredients = cur.fetchall()
    cur.close()

    ingredients_list = []
    for ingredient in ingredients:
        ingredients_list.append({
            "ingredient_id": ingredient[0],
            "ingredient_name": ingredient[1],
            "efficacy": ingredient[2],
            "contraindications": ingredient[3],
            "type": ingredient[4],
            "nutritions": ingredient[5],
            "unit_heat": ingredient[6],
            "created_at": ingredient[7],
            "updated_at": ingredient[8]
        })

    return jsonify(ingredients_list), 200

# 查询单个食材
@ingredients_blueprint.route('/ingredients/<int:ingredientId>', methods=['GET'])
def get_ingredient(ingredientId):
    cur = mysql.connection.cursor()

    # 构造 SQL 查询
    query = "SELECT * FROM ingredients WHERE ingredient_id = %s"
    cur.execute(query, (ingredientId,))
    ingredient_info = cur.fetchone()
    cur.close()

    if ingredient_info:
        return jsonify({
            "ingredient_id": ingredient_info[0],
            "ingredient_name": ingredient_info[1],
            "efficacy": ingredient_info[2],
            "contraindications": ingredient_info[3],
            "type": ingredient_info[4],
            "nutritions": ingredient_info[5],
            "url": ingredient_info[6],
            "created_at": ingredient_info[7],
            "updated_at": ingredient_info[8]
        }), 200
    else:
        return jsonify({"message": "食材信息不存在"}), 404

# 更新食材
@ingredients_blueprint.route('/ingredients/<int:ingredientId>', methods=['PUT'])
def update_ingredient(ingredientId):
    data = request.get_json()  # 获取 JSON 格式的请求数据
    cur = mysql.connection.cursor()

    # 构建更新语句，仅更新用户提供的信息
    updates = []
    params = []

    if 'ingredient_name' in data:
        updates.append("ingredient_name = %s")
        params.append(data['ingredient_name'])
    if 'efficacy' in data:
        updates.append("efficacy = %s")
        params.append(data['efficacy'])
    if 'contraindications' in data:
        updates.append("contraindications = %s")
        params.append(data['contraindications'])
    if 'type' in data:
        updates.append("type = %s")
        params.append(data['type'])
    if 'nutritions' in data:
        updates.append("nutritions = %s")
        params.append(data['nutritions'])
    if 'unit_heat' in data:
        updates.append("unit_heat = %s")
        params.append(data['unit_heat'])

    # 如果没有要更新的信息，返回错误
    if not updates:
        return jsonify({'message': 'No update information provided!'}), 400

    # 添加更新时间
    updates.append("updated_at = NOW()")
    params.append(ingredientId)  # 添加ingredientId作为查询条件

    # 构建完整的更新语句
    query = "UPDATE ingredients SET " + ", ".join(updates) + " WHERE ingredient_id = %s"
    cur.execute(query, tuple(params))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Ingredient not found or not updated!'}), 404
    else:
        return jsonify({'message': 'Ingredient updated successfully!'}), 200

# 删除食材
@ingredients_blueprint.route('/ingredients/<int:ingredientId>', methods=['DELETE'])
def delete_ingredient(ingredientId):
    cur = mysql.connection.cursor()

    # 构造 SQL 查询
    query = "DELETE FROM ingredients WHERE ingredient_id = %s"
    cur.execute(query, (ingredientId,))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Ingredient not found!'}), 404
    else:
        return jsonify({'message': 'Ingredient deleted successfully!'}), 200
#随机食材*3
@ingredients_blueprint.route('/ingredients/random3', methods=['GET'])
def get_random_ingredients():
    cur = mysql.connection.cursor()

    try:
        # 查询所有食材的 ID
        cur.execute("SELECT ingredient_id FROM ingredients")
        ingredient_ids = [row[0] for row in cur.fetchall()]

        # 随机选择三个 ID
        random_ids = random.sample(ingredient_ids, min(3, len(ingredient_ids)))

        # 根据随机 ID 查询对应的食材信息
        placeholders = ', '.join(['%s'] * len(random_ids))
        query = f"SELECT ingredient_id, ingredient_name, type, url FROM ingredients WHERE ingredient_id IN ({placeholders})"
        cur.execute(query, random_ids)
        ingredients = cur.fetchall()

        # 关闭游标
        cur.close()

        # 将结果转换为 JSON 格式
        result = [
            {
                "ingredient_id": row[0],
                "ingredient_name": row[1],
                "type": row[2],
                "url": row[3]
            }
            for row in ingredients
        ]
        return jsonify(result), 200
    except Exception as e:
        cur.close()
        return jsonify({"message": "Error fetching random ingredients", "error": str(e)}), 500

#根据标签查找食材
@ingredients_blueprint.route('/ingredients/tags', methods=['GET'])
def get_ingredients_by_tags():
    tag_query = request.args.get('tags')  # 从查询参数中获取标签
    if not tag_query:
        return jsonify({'message': '标签参数不能为空'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    try:
        # 构造 SQL 查询
        query = """
        SELECT * FROM ingredients 
        WHERE tags LIKE %s
        """
        cur.execute(query, ('%' + tag_query + '%',))
        ingredients = cur.fetchall()
        cur.close()

        ingredients_list = []
        for ingredient in ingredients:
            ingredients_list.append({
                "ingredient_id": ingredient[0],
                "ingredient_name": ingredient[1],
                "efficacy": ingredient[2],
                "contraindications": ingredient[3],
                "type": ingredient[4],
                "nutritions": ingredient[5],
                "unit_heat": ingredient[6],
                "created_at": ingredient[7],
                "updated_at": ingredient[8]
            })

        return jsonify(ingredients_list), 200
    except Exception as e:
        # 打印异常信息到服务器日志
        cur.close()
        return jsonify({"message": "查询食材时发生错误", "error": str(e)}), 500