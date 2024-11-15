import requests
import json

# 基础 URL，假设您的 Flask 应用正在本地运行且端口为 5000
BASE_URL = 'http://127.0.0.1:5000'

# 用户打卡 API 测试
def test_create_log():
    url = f'{BASE_URL}/user/1/log'
    payload = {
        'year': 2024,
        'month': 11,
        'log_days': {
            '1': 'Present',
            '2': 'Absent'
        }
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        print('Create log test passed!')
    else:
        print('Create log test failed!', response.text)

# 查询用户打卡记录 API 测试
def test_get_logs():
    url = f'{BASE_URL}/user/1/logs'
    response = requests.get(url)
    if response.status_code == 200:
        print('Get logs test passed!')
        print(response.json())  # 打印获取到的日志数据
    else:
        print('Get logs test failed!', response.text)

# 更新用户打卡记录 API 测试
def test_update_log():
    url = f'{BASE_URL}/user/1/log/1'
    payload = {
        'log_days': {
            '1': 'Present',
            '2': 'Present',
            '3': 'Absent'
        }
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print('Update log test passed!')
    else:
        print('Update log test failed!', response.text)

# 运行测试
if __name__ == '__main__':
    test_create_log()
    test_get_logs()
    test_update_log()