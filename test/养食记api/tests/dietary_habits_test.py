import requests
import json

# 测试服务器的 URL
# BASE_URL = 'http://127.0.0.1:5000'  # 确保端口号与 Flask 应用的端口号一致
BASE_URL = 'http://129.204.151.245:5001'
# 用户饮食习惯信息创建测试
def test_create_user_dietary_habits(userId):
    test_data = {
        'diet_goals': 'Healthy weight loss',
        'taste_preference': 'Spicy',
        'avoid_certain_food': 'Gluten',
        'fitness_planning': 'Weekly runs',
        'exercise_habits': 'Gym 3 times a week'
    }
    response = requests.post(f'{BASE_URL}/user/{userId}/dietary-habits', json=test_data)
    assert response.status_code == 201
    print('用户饮食习惯信息创建测试通过')

# 用户饮食习惯信息获取测试
def test_get_user_dietary_habits():
    response = requests.get(f'{BASE_URL}/user/1/dietary-habits')
    assert response.status_code == 200
    print('用户饮食习惯信息获取测试通过')

# 用户饮食习惯信息更新测试
def test_update_user_dietary_habits(userId):
    test_data = {
        'diet_goals': 'Maintain current weight',
        'taste_preference': 'Sweet',
        'avoid_certain_food': 'Dairy',
        'fitness_planning': 'Daily walks',
        'exercise_habits': 'Yoga 5 times a week'
    }
    response = requests.put(f'{BASE_URL}/user/{userId}/dietary-habit', json=test_data)
    assert response.status_code == 200
    print('用户饮食习惯信息更新测试通过')

# 用户饮食习惯信息删除测试
def test_delete_user_dietary_habits(userId):
    response = requests.delete(f'{BASE_URL}/user/{userId}/dietary-habit')
    assert response.status_code == 200
    print('用户饮食习惯信息删除测试通过')

# 运行所有测试
def run_tests():
    userId=2
    test_create_user_dietary_habits(userId)
    test_get_user_dietary_habits()
    test_update_user_dietary_habits(userId)
    test_delete_user_dietary_habits(userId)
if __name__ == '__main__':
    run_tests()