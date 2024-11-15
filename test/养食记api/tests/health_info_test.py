import requests
import json

# 测试服务器的 URL
# BASE_URL = 'http://127.0.0.1:5000'  # 确保端口号与 Flask 应用的端口号一致
BASE_URL = 'http://129.204.151.245:5001'
# 用户健康信息创建测试
def test_create_user_health_info(userId):
    test_data = {
        'blood_sugar': '100',
        'blood_pressure': '120/80 ',
        'allergens': 'Penicillin',
        'recent_medications': 'Ibuprofen',
        'past_medical_history': 'Appendectomy'
    }
    response = requests.post(f'{BASE_URL}/user/1/health-info', json=test_data)
    assert response.status_code == 201
    print('用户健康信息创建测试通过')

# 用户健康信息获取测试
def test_get_user_health_info(userId):
    response = requests.get(f'{BASE_URL}/user/1/health-infos')
    assert response.status_code == 200
    print('用户健康信息获取测试通过')

# 用户健康信息更新测试
def test_update_user_health_info(userId):
    test_data = {
        'blood_sugar': '95',
        'blood_pressure': '115/75',
        'allergens': 'None',
        'recent_medications': 'Acetaminophen',
        'past_medical_history': 'None'
    }
    response = requests.put(f'{BASE_URL}/user/1/health-info', json=test_data)
    assert response.status_code == 200
    print('用户健康信息更新测试通过')

# 用户健康信息删除测试
def test_delete_user_health_info():
    response = requests.delete(f'{BASE_URL}/user/1/health-info')
    assert response.status_code == 200
    print('用户健康信息删除测试通过')

# 运行所有测试
def run_tests():
    test_create_user_health_info()
    test_get_user_health_info()
    test_update_user_health_info()
    test_delete_user_health_info()

if __name__ == '__main__':
    run_tests()