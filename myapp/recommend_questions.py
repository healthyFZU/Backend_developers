from flask import Blueprint, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

# 创建 Blueprint
question_blueprint = Blueprint('questions', __name__)

# 初始化 MySQL
mysql = MySQL()


@question_blueprint.route('/questions/random', methods=['GET'])
def get_random_questions():
    """
    获取随机问题 API
    """
    try:
        # 创建数据库游标
        cur = mysql.connection.cursor()

        # 查询随机问题
        cur.execute("SELECT question_text FROM questions ORDER BY RAND() LIMIT 4")
        random_questions = [row[0] for row in cur.fetchall()]  # 获取结果

        cur.close()  # 关闭游标

        # 返回查询结果
        return jsonify({"questions": random_questions}), 200

    except Exception as e:
        print(f"发生错误: {e}")
        return jsonify({"error": "无法获取随机问题"}), 500
