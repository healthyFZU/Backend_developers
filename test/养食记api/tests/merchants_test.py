import requests
import json

# 测试服务器地址
#BASE_URL = 'http://127.0.0.1:5000'  # 请确保这是正确的测试服务器地址
BASE_URL = 'http://129.204.151.245:5001'

# 创建商家
def test_create_merchant():
    data = {
        'merchant_name': 'Test Merchant',
        'address': '123 Test Street',
        'logo': 'test_logo.png',
        'menu': {'item1': 'Test Item 1'}
    }
    response = requests.post(BASE_URL + '/merchants', json=data)
    print('Status Code:', response.status_code)
    if response.status_code == 201:
        print('Create Merchant Response:', response.json())  # 如果状态码为201，表示创建成功

# 获取单个商家
def test_get_merchant(merchant_id):
    response = requests.get(BASE_URL + '/merchants/' + str(merchant_id))
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Get Merchant Response:', response.json())  # 如果状态码为200，表示获取成功

# 获取所有商家
def test_get_merchants():
    response = requests.get(BASE_URL + '/merchants')
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Get Merchants Response:', response.json())  # 如果状态码为200，表示获取成功

# 更新商家信息
def test_update_merchant(merchant_id):
    data = {
        'merchant_name': 'Updated Test Merchant',
        'address': '456 Updated Street'
    }
    response = requests.put(BASE_URL + '/merchants/' + str(merchant_id), json=data)
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Update Merchant Response:', response.json())  # 如果状态码为200，表示更新成功
    else:
        print('Error Response:', response.json())  # 如果状态码不是200，打印错误信息
# 删除商家
def test_delete_merchant(merchant_id):
    response = requests.delete(BASE_URL + '/merchants/' + str(merchant_id))
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Delete Merchant Response:', response.json())  # 如果状态码为200，表示删除成功

# 运行测试
if __name__ == '__main__':
    #test_create_merchant()  # 测试创建商家
    merchant_id = 7  # 假设创建后获取的商家ID为1
    test_get_merchant(merchant_id)  # 测试获取单个商家
    test_get_merchants()  # 测试获取所有商家
    #test_update_merchant(merchant_id)  # 测试更新商家信息
    #test_delete_merchant(merchant_id)  # 测试删除商家