# myapp/user.py
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager

user_blueprint = Blueprint('user', __name__)

mysql = MySQL()
bcrypt =Bcrypt()
jwt = JWTManager()
# 用户注册 API
@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("Received data:", data)  # 调试用，打印接收到的数据
    phoneNum = data.get('phoneNum')
    password = data.get('password')

    # 检查必填字段
    if not phoneNum or not password:
        return jsonify({'message': 'All fields are required!'}), 400

    # 密码加密
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # 连接数据库
    cur = mysql.connection.cursor()

    # 检查用户是否已存在
    cur.execute("SELECT * FROM user_info WHERE phoneNum = %s", (phoneNum,))
    user = cur.fetchone()

    if user:
        return jsonify({'message': 'Username or phone number already exists.'}), 400

    # 插入新用户
    cur.execute("INSERT INTO user_info (phoneNum, password,avatar_url,nickname,birthday) VALUES (%s,%s,%s,%s,%s)", (phoneNum, hashed_password,'https://example.com/avatar01.jpg','Fzuer','2004-11-11'))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User registered successfully!'}), 201

# 用户登录 API
@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phoneNum = data.get('phoneNum')
    password = data.get('password')

    # 检查必填字段
    if not phoneNum or not password:
        return jsonify({'message': 'Both phone number and password are required!'}), 400

    # 连接数据库
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_info WHERE phoneNum = %s", (phoneNum,))
    user = cur.fetchone()

    # 验证用户密码
    if user and bcrypt.check_password_hash(user[1], password):  # user[1] 是密码
        # 生成 JWT
        access_token = create_access_token(identity=phoneNum)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401

# 查看用户信息 API
@user_blueprint.route('/profile', methods=['GET'])
@jwt_required()  # 确保用户已登录
def profile():
    # 获取 JWT 中的身份信息
    current_user = get_jwt_identity()

    # 连接数据库
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_info WHERE phoneNum = %s", (current_user,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({'message': 'User not found!'}), 404

    # 将查询结果转换为字典
    user_data = {
        'Id': user[0],  # 假设 id 是第一个字段
        'phoneNum': user[2],  # 假设 phoneNum 是第二个字段
        'password': user[1],  # 假设 password 是第三个字段
        'avatar_url': user[3],
        'nickname': user[4],
        'created_at': user[5],
        'updated_at':user[6],
        'birthday':user[7]
        # 这里可以继续添加其他字段，确保顺序与数据库表一致
    }

    return jsonify(user_data), 200

# 修改用户信息 API
@user_blueprint.route('/update', methods=['PUT'])
@jwt_required()  # 确保请求携带有效的 JWT
def update_user():
    # 获取当前登录用户的 phoneNum
    current_user = get_jwt_identity()
    data = request.get_json()

    new_avatar_url = data.get('avatar_url')
    new_nickname = data.get('nickname')
    new_birthday = data.get('birthday')
    new_password = data.get('password')

    # 连接数据库
    cur = mysql.connection.cursor()

    # 检查是否有需要更新的字段
    updates = []
    update_values = []

    if new_password:
        # 密码加密
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        updates.append("password = %s")
        update_values.append(hashed_password)

    if new_avatar_url:
        updates.append("avatar_url = %s")
        update_values.append(new_avatar_url)

    if new_nickname:
        updates.append("nickname = %s")
        update_values.append(new_nickname)

    if new_birthday:
        updates.append("birthday = %s")
        update_values.append(new_birthday)

    # 如果没有需要更新的字段，返回 400 错误
    if not updates:
        return jsonify({'message': 'No data to update!'}), 400

    # 构建更新的 SQL 语句
    update_values.append(current_user)  # 将当前用户的 phoneNum 作为 WHERE 条件
    update_query = f"UPDATE user_info SET {', '.join(updates)} WHERE phoneNum = %s"

    # 执行更新
    cur.execute(update_query, tuple(update_values))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User information updated successfully!'}), 200
