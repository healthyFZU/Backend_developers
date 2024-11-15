import requests
import json

# 测试服务器的 URL
# BASE_URL = 'http://127.0.0.1:5000'  # 确保端口号与 Flask 应用的端口号一致
BASE_URL = 'http://129.204.151.245:5001'
# 用户身体信息创建测试
def test_create_user_body_info():
    test_data = {
        'age': 30,
        'sex': '男',
        'height': 1.75,
        'weight': 70,
        'weight_target': 65,
        'target': '减重5公斤',
        'stage': '第一阶段',
        'pre_over_time': '2024-12-31'
    }
    response = requests.post(f'{BASE_URL}/user/1/body-info', json=test_data)
    assert response.status_code == 201
    print('用户身体信息创建测试通过')

# 用户身体信息获取测试
def test_get_user_body_info():
    response = requests.get(f'{BASE_URL}/user/1/body-info')
    assert response.status_code == 200
    print('用户身体信息获取测试通过')

# 用户身体信息更新测试
def test_update_user_body_info():
    test_data = {
        'age': 31,
        'sex': '男',
        'height': 1.76,
        'weight': 68,
        'weight_target': 68,
        'target': '维持体重',
        'stage': '第二阶段',
        'pre_over_time': '2025-01-01'
    }
    response = requests.put(f'{BASE_URL}/user/1/body-info', json=test_data)
    assert response.status_code == 200
    print('用户身体信息更新测试通过')

# 用户身体信息删除测试
def test_delete_user_body_info():
    response = requests.delete(f'{BASE_URL}/user/1/body-info')
    assert response.status_code == 200
    print('用户身体信息删除测试通过')

# 运行所有测试
def run_tests():
    test_create_user_body_info()
    test_get_user_body_info()
    test_update_user_body_info()
    test_delete_user_body_info()

if __name__ == '__main__':
    run_tests()