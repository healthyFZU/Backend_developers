import requests
import json

# 测试服务器的 URL
BASE_URL = 'http://127.0.0.1:5000'


# 用户注册测试
def test_user_registration():
    # 测试数据
    test_data = {
        'phoneNum': '1234567890',
        'password': 'password123'
    }

    # 发送 POST 请求到注册 API
    response = requests.post(BASE_URL + '/user/register', json=test_data)

    # 检查响应状态码
    if response.status_code != 201:
        print("Register Response Status Code:", response.status_code)
        print("Register Response Text:", response.text)
        return

    try:
        # 尝试解析响应内容为 JSON
        response_json = response.json()
        print("Register Response:", response_json)
    except json.JSONDecodeError:
        print("Register Response is not JSON")


# 用户登录测试
def test_user_login():
    # 测试数据（使用注册时的用户名和密码）
    test_data = {
        'phoneNum': '1234567890',
        'password': 'password123'
    }

    # 发送 POST 请求到登录 API
    response = requests.post(BASE_URL + '/user/login', json=test_data)

    # 检查响应状态码
    if response.status_code != 200:
        print("Login Response Status Code:", response.status_code)
        print("Login Response Text:", response.text)
        return

    try:
        # 尝试解析响应内容为 JSON
        response_json = response.json()
        print("Login Response:", response_json)
    except json.JSONDecodeError:
        print("Login Response is not JSON")


# 运行测试
if __name__ == '__main__':
    test_user_registration()
    test_user_login()