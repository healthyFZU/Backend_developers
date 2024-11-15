import requests
import json

# 测试服务器地址
BASE_URL = 'http://www.yangshiji.icu:5001'  # 请确保这是正确的测试服务器地址

# 获取所有菜品
def test_get_dishes():
    response = requests.get(BASE_URL + '/dishes')
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Get Dishes Response:', response.json())  # 如果状态码为200，表示获取成功

# 获取单个菜品
def test_get_dish(dish_id):
    response = requests.get(BASE_URL + '/dishes/' + str(dish_id))
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('Get Dish Response:', response.json())  # 如果状态码为200，表示获取成功



# 运行测试
if __name__ == '__main__':

    # dish_id = response.json()['dish_id']  # 假设创建后获取的菜品ID
    dish_id =17
    test_get_dish(dish_id)  # 测试获取单个菜品
    test_get_dishes()  # 测试获取所有菜品
