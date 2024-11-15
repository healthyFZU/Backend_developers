import requests

# 测试服务器地址
BASE_URL = 'http://127.0.0.1:5000'

# 创建用户评价
def test_create_review():
    data = {
        'score': 5,
        'dish_id': 18,
        'review': '非常好吃！'
    }
    response = requests.post(BASE_URL + '/user/1/review', json=data)
    print('Create Review Status Code:', response.status_code)
    if response.status_code == 201:
        print('Create Review Response:', response.json())
    else:
        print('Create Review Response Text:', response.text)

# 获取用户评价
def test_get_review(review_id):
    response = requests.get(BASE_URL + f'/user/1/review/{review_id}')
    print('Get Review Status Code:', response.status_code)
    if response.status_code == 200:
        print('Get Review Response:', response.json())
    else:
        print('Get Review Response Text:', response.text)

# 更新用户评价
def test_update_review(review_id):
    data = {
        'score': 4  # 假设我们只想更新评分
    }
    response = requests.put(BASE_URL + f'/user/1/review/{review_id}', json=data)
    print('Update Review Status Code:', response.status_code)
    if response.status_code == 200:
        print('Update Review Response:', response.json())
    else:
        print('Update Review Response Text:', response.text)

# 删除用户评价
def test_delete_review(review_id):
    response = requests.delete(BASE_URL + f'/user/1/review/{review_id}')
    print('Delete Review Status Code:', response.status_code)
    if response.status_code == 200:
        print('Delete Review Response:', response.json())
    else:
        print('Delete Review Response Text:', response.text)

# 运行测试
if __name__ == '__main__':
    # 测试创建用户评价
    test_create_review()
    test_get_review(9)
    test_update_review(9)
    test_delete_review(13)