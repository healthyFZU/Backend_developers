from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import json
from flask import current_app as app

body_measurements_blueprint = Blueprint('body_measurements', __name__)

mysql = MySQL()

# 创建用户身体测量信息 API
@body_measurements_blueprint.route('/user/<int:userId>/measurements', methods=['POST'])
def create_user_measurements(userId):
    data = request.get_json()

    # 获取新数据
    waist = json.dumps(data.get('waist', []))
    thigh = json.dumps(data.get('thigh', []))
    calf = json.dumps(data.get('calf', []))
    bust = json.dumps(data.get('bust', []))
    hips = json.dumps(data.get('hips', []))
    arm = json.dumps(data.get('arm', []))
    dates = json.dumps(data.get('dates', [datetime.now().strftime('%Y-%m-%d')]))
    created_at = datetime.now()
    updated_at = datetime.now()

    cur = mysql.connection.cursor()
    try:
        # 插入新记录
        cur.execute(
            """
            INSERT INTO body_measurements (userId, waist, thigh, calf, bust, hips, arm, dates, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (userId, waist, thigh, calf, bust, hips, arm, dates, created_at, updated_at)
        )
        mysql.connection.commit()
        measurement_id = cur.lastrowid
        cur.close()
        return jsonify({'message': 'New measurement created!', 'measurement_id': measurement_id}), 201
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return jsonify({'message': 'Failed to create measurement', 'error': str(e)}), 500

# 获取用户身体测量信息 API
@body_measurements_blueprint.route('/user/<int:userId>/measurements', methods=['GET'])
def get_user_measurements(userId):
    cur = mysql.connection.cursor()

    # 查询用户身体测量信息记录，按 updated_at 升序排列
    cur.execute(
        "SELECT * FROM body_measurements WHERE userId = %s ORDER BY updated_at ASC",
        (userId,)
    )
    measurements = cur.fetchall()
    cur.close()

    # 如果没有数据，返回默认的空值
    if not measurements:
        return jsonify([]), 200

    # 解析 JSON 字段的辅助函数
    def parse_json_field(field):
        try:
            return json.loads(field) if field else []
        except (TypeError, json.JSONDecodeError):
            return []

    # 格式化日期字段的辅助函数
    def format_datetime_field(field):
        return field.strftime('%Y-%m-%d %H:%M:%S') if isinstance(field, datetime) else ''

    # 构造返回数据列表
    records = []
    for measurement in measurements:
        records.append({
            'measurement_id': measurement[0],
            'userId': measurement[1],
            'waist': parse_json_field(measurement[2]),
            'thigh': parse_json_field(measurement[3]),
            'calf': parse_json_field(measurement[4]),
            'bust': parse_json_field(measurement[5]),
            'hips': parse_json_field(measurement[6]),
            'arm': parse_json_field(measurement[7]),
            'dates': format_datetime_field(measurement[9]),  # 使用 updated_at 作为日期
            'created_at': format_datetime_field(measurement[8]),
            'updated_at': format_datetime_field(measurement[9])
        })

    # 返回所有历史记录
    return jsonify(records), 200

@body_measurements_blueprint.route('/user/<int:userId>/measurements', methods=['PUT'])
def update_user_measurements(userId):
    data = request.get_json()

    # 定义可更新字段
    fields = ['waist', 'thigh', 'calf', 'bust', 'hips', 'arm']

    # 查询原始记录
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM body_measurements WHERE userId = %s ORDER BY created_at DESC LIMIT 1", (userId,))
    original_record = cur.fetchone()

    if not original_record:
        cur.close()
        return jsonify({'message': 'Original record not found!'}), 404

    # 获取当前时间戳
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 构造更新记录
    try:
        update_query = """
            UPDATE body_measurements
            SET {} WHERE userId = %s
        """
        update_clauses = []
        update_values = []

        for field in fields:
            if field in data:
                # 获取原始 JSON 数据并追加新值
                original_json = original_record[fields.index(field) + 2]  # 假设字段从第 2 列开始
                original_dict = json.loads(original_json) if original_json else {}
                original_dict[timestamp] = data[field]  # 将时间戳作为 key, 新值作为 value
                update_clauses.append(f"{field} = %s")
                update_values.append(json.dumps(original_dict))

        if not update_clauses:
            cur.close()
            return jsonify({'message': 'No updates provided!'}), 400

        # 添加更新时间
        update_clauses.append("updated_at = %s")
        update_values.append(datetime.now())

        # 完整 SQL
        update_query = update_query.format(", ".join(update_clauses))
        update_values.append(userId)

        # 执行更新操作
        cur.execute(update_query, tuple(update_values))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Record updated successfully!'}), 200

    except Exception as e:
        app.logger.error(f"Error updating measurement: {str(e)}")
        mysql.connection.rollback()
        cur.close()
        return jsonify({'message': 'Failed to update record.', 'error': str(e)}), 500


# 删除用户身体测量信息 API
@body_measurements_blueprint.route('/user/<int:userId>/measurements/<int:measurement_id>', methods=['DELETE'])
def delete_user_measurements(userId, measurement_id):
    cur = mysql.connection.cursor()

    # 删除用户身体测量信息记录
    cur.execute("DELETE FROM body_measurements WHERE userId = %s AND measurement_id = %s", (userId, measurement_id))
    mysql.connection.commit()
    cur.close()

    if cur.rowcount == 0:
        return jsonify({'message': 'Measurements not found!'}), 404
    else:
        return jsonify({'message': 'Measurements deleted successfully!'}), 200
