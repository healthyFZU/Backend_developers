import requests
import time
# 设置基础 URL
# base_url = 'http://127.0.0.1:5000'
base_url = 'http://129.204.151.245:5001'

# 用户注册测试
def test_register():
    url = f'{base_url}/user/register'
    data = {
        'phoneNum': '1234567890788',
        'password': 'password123'
    }

    response = requests.post(url, json=data)
    print("Register Response:", response.json())
    assert response.status_code == 201  # 期待状态码是 201，表示创建成功


# 用户登录测试
def test_login():
    url = f'{base_url}/user/login'
    data = {
        'phoneNum': '1234567890',
        'password': 'password123'
    }

    response = requests.post(url, json=data)
    print("Login Response:", response.json())

    # 检查是否返回 JWT Token
    assert response.status_code == 200
    assert 'access_token' in response.json()

    return response.json()['access_token']  # 返回 JWT Token，用于后续测试


# 查看用户信息测试
def test_profile(access_token):
    url = f'{base_url}/user/profile'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    print("Profile Response:", response.json())
    assert response.status_code == 200  # 期待状态码是 200，表示请求成功


# 修改用户信息测试
def test_update_user(access_token):
    url = f'{base_url}/user/update'
    data = {
        'phoneNum': '1234567890',
        'password': 'newpassword123'
    }

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.put(url, json=data, headers=headers)
    print("Update User Response:", response.json())
    assert response.status_code == 200  # 期待状态码是 200，表示更新成功


# 测试流程
def run_tests():
    # 1. 用户注册
    test_register()
    time.sleep(2)
    # 2. 用户登录并获取 JWT Token
    access_token = test_login()
    time.sleep(2)
    # 3. 查看用户信息
    test_profile(access_token)
    time.sleep(2)
    # 4. 修改用户信息
    test_update_user(access_token)
    time.sleep(2)
    # 5. 重新查看用户信息，确保密码已修改
    test_profile(access_token)
    time.sleep(2)

if __name__ == '__main__':
    run_tests()
