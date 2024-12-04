import os
import sys

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目的根目录
root_dir = os.path.dirname(current_dir)

# 将根目录添加到 sys.path
sys.path.append(root_dir)

# 现在可以安全地导入 create_app
from myapp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True,threaded=True)
