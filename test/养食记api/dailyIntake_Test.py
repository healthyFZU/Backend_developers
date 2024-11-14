import requests

# 测试服务器地址
BASE_URL = 'http://127.0.0.1:5000'


# 创建用户每日摄入记录
def test_create_daily_intake():
    data = {
        'intake_date': '2024-11-12',
        'water_target': 2000,
        'have_drunk': 1500,
        'energy_target': 2500,
        'energy_consumed': 2200
    }
    response = requests.post(BASE_URL + '/user/1/intake', json=data)
    print('Create Daily Intake Status Code:', response.status_code)
    if response.status_code == 201:
        response_data = response.json()
        print('Create Daily Intake Response:', response_data)
        return response_data.get('intake_id')  # 返回intake_id
    return None


# 获取用户每日摄入记录
def test_get_daily_intake(intake_id):
    if intake_id is None:
        print('Intake ID is None. Skipping get request.')
        return
    response = requests.get(BASE_URL + f'/user/1/intake/{intake_id}')
    print('Get Daily Intake Status Code:', response.status_code)
    if response.status_code == 200:
        print('Get Daily Intake Response:', response.json())
    else:
        print('Get Daily Intake Response Text:', response.text)


# 更新用户每日摄入记录
def test_update_daily_intake(intake_id):
    if intake_id is None:
        print('Intake ID is None. Skipping update request.')
        return
    data = {
        'have_drunk': 1800  # 假设我们只想更新已饮水量
    }
    response = requests.put(BASE_URL + f'/user/1/intake/{intake_id}', json=data)
    print('Update Daily Intake Status Code:', response.status_code)
    if response.status_code == 200:
        print('Update Daily Intake Response:', response.json())
    else:
        print('Update Daily Intake Response Text:', response.text)


# 删除用户每日摄入记录
def test_delete_daily_intake(intake_id):
    if intake_id is None:
        print('Intake ID is None. Skipping delete request.')
        return
    response = requests.delete(BASE_URL + f'/user/1/intake/{intake_id}')
    print('Delete Daily Intake Status Code:', response.status_code)
    if response.status_code == 200:
        print('Delete Daily Intake Response:', response.json())
    else:
        print('Delete Daily Intake Response Text:', response.text)


# 获取特定日期的用户每日摄入记录
def test_get_daily_intake_by_date(date):
    response = requests.get(BASE_URL + f'/user/1/intake/date/{date}')
    print('Get Daily Intake By Date Status Code:', response.status_code)
    if response.status_code == 200:
        print('Get Daily Intake By Date Response:', response.json())
    else:
        print('Get Daily Intake By Date Response Text:', response.text)


# 运行测试
if __name__ == '__main__':
    intake_id = test_create_daily_intake()  # 存储创建响应的intake_id
    if intake_id:
        print(f'Intake ID: {intake_id}')
        # 测试获取用户每日摄入记录
        test_get_daily_intake(intake_id)
        # 测试更新用户每日摄入记录
        test_update_daily_intake(intake_id)
        # 测试删除用户每日摄入记录
        test_delete_daily_intake(intake_id)
    else:
        print(f'Intake ID: {intake_id}')

    # 测试获取特定日期的用户每日摄入记录
    test_get_daily_intake_by_date('2024-11-12')