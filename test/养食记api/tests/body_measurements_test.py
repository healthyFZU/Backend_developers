import requests
import json

# 测试服务器的 URL
# BASE_URL = 'http://127.0.0.1:5000'  # 确保端口号与 Flask 应用的端口号一致
BASE_URL = 'http://129.204.151.245:5001'
# 用户身体测量信息创建测试
def test_create_user_measurements():
    test_data = {
        'waist': 80,
        'thigh': 60,
        'calf': 40,
        'bust': 90,
        'hips': 95,
        'arm': 30
    }
    response = requests.post(f'{BASE_URL}/user/1/measurements', json=test_data)
    assert response.status_code == 201
    print('用户身体测量信息创建测试通过')

# 用户身体测量信息获取测试
def test_get_user_measurements():
    response = requests.get(f'{BASE_URL}/user/1/measurements')
    assert response.status_code == 200
    print('用户身体测量信息获取测试通过')

# 用户身体测量信息更新测试
def test_update_user_measurements():
    test_data = {
        'waist': 81,
        'thigh': 61,
        'calf': 41,
        'bust': 91,
        'hips': 96,
        'arm': 31
    }
    measurement_id = 1  # 假设要更新的测量信息 ID 为 1
    response = requests.put(f'{BASE_URL}/user/1/measurements/{measurement_id}', json=test_data)
    assert response.status_code == 200
    print('用户身体测量信息更新测试通过')

# 用户身体测量信息删除测试
def test_delete_user_measurements():
    measurement_id = 1  # 假设要删除的测量信息 ID 为 1
    response = requests.delete(f'{BASE_URL}/user/1/measurements/{measurement_id}')
    assert response.status_code == 200
    print('用户身体测量信息删除测试通过')

# 运行所有测试
def run_tests():
    test_create_user_measurements()
    test_get_user_measurements()
    test_update_user_measurements()
    test_delete_user_measurements()

if __name__ == '__main__':
    run_tests()