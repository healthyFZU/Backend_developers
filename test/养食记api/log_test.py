import requests
import json

# 测试服务器地址
BASE_URL = 'http://127.0.0.1:5000'

# 创建打卡记录
def test_create_log():
    data = {
        'year': 2024,
        'month': 11,
        'log_days': {'1': 'Present', '2': 'Absent'}  # 假设的打卡数据
    }
    response = requests.post(BASE_URL + '/user/log', json=data)
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Create Log Response:', response.json())  # 如果状态码为200，则解析JSON

# 获取打卡记录
def test_get_logs():
    response = requests.get(BASE_URL + '/user/logs')
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Get Logs Response:', response.json())  # 如果状态码为200，则解析JSON

# 更新打卡记录
def test_update_log(log_id):
    data = {
        'log_days': {'1': 'Present', '3': 'Present'}  # 更新后的打卡数据
    }
    response = requests.put(BASE_URL + '/user/log/{}'.format(log_id), json=data)
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Update Log Response:', response.json())  # 如果状态码为200，则解析JSON

# 运行测试
if __name__ == '__main__':
    test_create_log()  # 测试创建打卡记录
    test_get_logs()   # 测试获取打卡记录
    # 测试更新打卡记录需要一个有效的log_id，这里假设log_id为1
    test_update_log(1)