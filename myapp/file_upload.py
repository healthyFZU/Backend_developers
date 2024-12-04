from flask import Blueprint, request, jsonify, send_from_directory, url_for,current_app as app
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import os

# 文件上传蓝图
file_upload_blueprint = Blueprint('file_upload', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
mysql = MySQL()
def allowed_file(filename):
    """检查文件是否符合允许的扩展名"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 文件上传接口
@file_upload_blueprint.route('/upload/<string:userId>', methods=['POST'])
def upload_file(userId):
    """处理文件上传并更新用户的头像 URL"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 保存文件
        file.save(filepath)

        # 返回文件的访问 URL
        file_url = url_for('file_upload.get_image', filename=filename, _external=True)

        # 连接数据库并更新用户的头像 URL
        cur = mysql.connection.cursor()

        try:
            # 更新用户的 avatar_url 字段
            cur.execute("""
                UPDATE user_info 
                SET avatar_url = %s 
                WHERE userId = %s
            """, (file_url, userId))
            mysql.connection.commit()

            return jsonify({'message': 'File uploaded successfully', 'url': file_url}), 200
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({'error': f'Error updating user avatar URL: {str(e)}'}), 500
        finally:
            cur.close()
    else:
        return jsonify({'error': 'File type not allowed'}), 400

# 获取文件接口
@file_upload_blueprint.route('/get_image/<filename>', methods=['GET'])
def get_image(filename):
    """接收图片名称，返回图片内容"""
    try:
        # 检查图片是否存在于上传目录
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        # 返回图片文件
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
