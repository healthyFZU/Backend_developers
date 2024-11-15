from flask import Flask, Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import json
app = Flask(__name__)

# 配置数据库
mysql = MySQL(app)

# 创建商家蓝图
merchants_blueprint = Blueprint('merchants', __name__)

@merchants_blueprint.route('/merchants', methods=['POST'])
def create_merchant():
    data = request.get_json()  # 获取 JSON 格式的请求数据

    # 获取商家信息
    merchant_name = data.get('merchant_name')
    address = data.get('address')
    logo = data.get('logo')
    menu = data.get('menu')

    # 检查必填字段
    if not all([merchant_name, address, logo, menu]):
        return jsonify({'message': 'All fields are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()

    try:
        # 构造 SQL 查询，不包括 created_at 和 updated_at 字段，因为它们会自动生成
        query = """
        INSERT INTO merchants (Merchant_name, address, logo, menu)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (merchant_name, address, logo, json.dumps(menu) if isinstance(menu, dict) else menu))

        mysql.connection.commit()
        new_merchant_id = cur.lastrowid  # 获取新创建记录的 ID
        cur.close()

        return jsonify({"message": "商家创建成功", "merchant_id": new_merchant_id}), 201
    except Exception as e:
        # 打印异常信息到服务器日志
        cur.close()
        return jsonify({"message": "An error occurred while creating the merchant.", "error": str(e)}), 500

#查询所有商家
@merchants_blueprint.route('/merchants', methods=['GET'])
def get_merchants():
    cur = mysql.connection.cursor()

    # 构造 SQL 查询
    query = "SELECT * FROM merchants"
    cur.execute(query)
    merchants = cur.fetchall()
    cur.close()

    merchants_list = []
    for merchant in merchants:
        merchants_list.append({
            "MerchantId": merchant[0],
            "Merchant_name": merchant[1],
            "address": merchant[2],
            "logo": merchant[3],
            "menu": merchant[4],
            "created_at": merchant[5],
            "updated_at": merchant[6]
        })

    return jsonify(merchants_list), 200
# 查询单个商家
@merchants_blueprint.route('/merchants/<int:merchantId>', methods=['GET'])
def get_merchant(merchantId):
    cur = mysql.connection.cursor()

    # 构造 SQL 查询
    query = "SELECT * FROM merchants WHERE MerchantId = %s"
    cur.execute(query, (merchantId,))
    merchant_info = cur.fetchone()
    cur.close()

    if merchant_info:
        return jsonify({
            "MerchantId": merchant_info[0],
            "Merchant_name": merchant_info[1],
            "address": merchant_info[2],
            "logo": merchant_info[3],
            "menu": merchant_info[6],
            "created_at": merchant_info[4],
            "updated_at": merchant_info[5]
        }), 200
    else:
        return jsonify({"message": "商家信息不存在"}), 404
#更新商家
@merchants_blueprint.route('/merchants/<int:merchantId>', methods=['PUT'])
def update_merchant(merchantId):
    data = request.get_json()  # 获取 JSON 格式的请求数据
    cur = mysql.connection.cursor()

    # 构建更新语句，仅更新用户提供的信息
    updates = []
    params = []

    if 'merchant_name' in data:
        updates.append("Merchant_name = %s")
        params.append(data['merchant_name'])
    if 'address' in data:
        updates.append("address = %s")
        params.append(data['address'])
    if 'logo' in data:
        updates.append("logo = %s")
        params.append(data['logo'])
    if 'menu' in data:
        updates.append("menu = %s")
        params.append(json.dumps(data['menu']) if isinstance(data['menu'], dict) else data['menu'])

    # 如果没有要更新的信息，返回错误
    if not updates:
        return jsonify({'message': 'No update information provided!'}), 400

    # 添加更新时间
    updates.append("updated_at = NOW()")

    # 添加merchantId作为查询条件
    params.append(merchantId)

    # 构建完整的更新语句
    query = "UPDATE merchants SET " + ", ".join(updates) + " WHERE MerchantId = %s"
    cur.execute(query, tuple(params))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Merchant not found or not updated!'}), 404
    else:
        return jsonify({'message': 'Merchant updated successfully!'}), 200
# 删除商家
@merchants_blueprint.route('/merchants/<int:merchantId>', methods=['DELETE'])
def delete_merchant(merchantId):
    cur = mysql.connection.cursor()

    # 构造 SQL 查询
    query = "DELETE FROM merchants WHERE MerchantId = %s"
    cur.execute(query, (merchantId,))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Merchant not found!'}), 404
    else:
        return jsonify({'message': 'Merchant deleted successfully!'}), 200



