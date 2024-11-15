import requests
import json

# 测试服务器地址
# BASE_URL = 'http://127.0.0.1:5000'  # 请确保这是正确的测试服务器地址
BASE_URL = 'http://129.204.151.245:5001'  # 请确保这是正确的测试服务器地址
# 创建食材
def test_create_ingredient():
    data = {
        'ingredient_name': 'Test Ingredient',
        'efficacy': 'Efficacy 1, Efficacy 2',
        'contraindications': 'Contra 1',
        'type': 'Test Type',
        'nutritions': 'Protein: 10, Fat: 5',
        'unit_heat': 100
    }
    response = requests.post(BASE_URL + '/ingredients', json=data)
    print('Status Code:', response.status_code)
    if response.status_code == 201:
        print('Create Ingredient Response:', response.json())  # 如果状态码为201，表示创建成功
        return response.json()['ingredient_id']
    else:
        print('Error Response:', response.json())  # 如果状态码不是201，打印错误信息

# 获取单个食材
def test_get_ingredient(ingredient_id):
    response = requests.get(BASE_URL + '/ingredients/' + str(ingredient_id))
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Get Ingredient Response:', response.json())  # 如果状态码为200，表示获取成功

# 获取所有食材
def test_get_ingredients(limit=None):
    url = BASE_URL + '/ingredients'
    if limit:
        url += '?limit=' + str(limit)
    response = requests.get(url)
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Get Ingredients Response:', response.json())  # 如果状态码为200，表示获取成功

# 更新食材信息
def test_update_ingredient(ingredient_id):
    data = {
        'ingredient_name': 'Updated Test Ingredient',
        'type': 'Updated Type'
    }
    response = requests.put(BASE_URL + '/ingredients/' + str(ingredient_id), json=data)
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Update Ingredient Response:', response.json())  # 如果状态码为200，表示更新成功
    else:
        print('Error Response:', response.json())  # 如果状态码不是200，打印错误信息

# 删除食材
def test_delete_ingredient(ingredient_id):
    response = requests.delete(BASE_URL + '/ingredients/' + str(ingredient_id))
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Delete Ingredient Response:', response.json())  # 如果状态码为200，表示删除成功

if __name__ == '__main__':
    # id=test_create_ingredient()
    id=100
    test_get_ingredient(id)
    test_get_ingredients()
    # test_update_ingredient(id)
    # test_delete_ingredient(id)