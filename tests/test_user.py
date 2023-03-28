"""

By Ziqiu Li
Created at 2023/3/24 17:55
"""
import unittest
from . import client, BASE_URL


admin_user_id = None
other_user_id = None


class testUser(unittest.TestCase):
    # 该测试单元不可在PyCharm 中直接运行
    # PyCharm 会自动进行优化
    # 导致无法按照测试顺序进行
    # 使用命令行进行测试
    # python test_excel.py

    @classmethod
    def setUpClass(cls) -> None:
        print('Test begin')

    @classmethod
    def tearDownClass(cls) -> None:
        print('Test end')

    def test_create_user_admin(self):
        global admin_user_id
        res = client.post(BASE_URL + '/user', json={
            'mail': 'admin@qiuying.com',
            'password': '123456',
            'is_admin': True
        })
        admin_user_id = res.get_json().get('data')
        self.assertEqual(res.status_code, 201)
        self.assertTrue(admin_user_id)

    def test_create_user(self):
        global other_user_id
        res = client.post(BASE_URL + '/user', json={
            'name': '李子秋',
            'mail': 'lcmail1001@163.com',
            'password': '654321',
            'is_admin': False
        })
        other_user_id = res.get_json().get('data')
        self.assertEqual(res.status_code, 201)
        self.assertTrue(other_user_id)

    def test_create_user_again(self):
        res = client.post(BASE_URL + '/user', json={
            'name': '李子秋',
            'mail': 'lcmail1001@163.com',
            'password': '1',
        })
        self.assertEqual(res.status_code, 409)

    def test_login_admin(self):
        res = client.post(BASE_URL + '/token', json={
            'mail': 'admin@qiuying.com',
            'password': '123456'
        })
        token = res.get_json().get('data').get('token')

        self.assertEqual(res.status_code, 200)
        self.assertTrue(token)

    def test_get_user_info(self):
        # admin
        res = client.get(BASE_URL + '/user/' + admin_user_id)
        admin_user_info = res.get_json().get('data')
        self.assertEqual('admin', admin_user_info['name'])
        self.assertEqual('admin@qiuying.com', admin_user_info['mail'])
        self.assertTrue(admin_user_info['is_admin'])
        self.assertEqual('123456', admin_user_info['password'])
        # other
        res = client.get(BASE_URL + '/user/' + other_user_id)
        other_user_info = res.get_json().get('data')
        self.assertEqual('李子秋', other_user_info['name'])
        self.assertFalse(other_user_info['is_admin'])

    def test_update_user(self):
        res = client.put(BASE_URL + '/user/' + other_user_id, json={
            'tel': '12345678901'
        })
        self.assertEqual(res.status_code, 200)
        res = client.get(BASE_URL + '/user/' + other_user_id)
        self.assertEqual('12345678901', res.get_json().get('data')['tel'])

    def test_get_all_users(self):
        res = client.get(BASE_URL + '/users')
        users = res.get_json().get('data')['users']
        self.assertEqual(1, len(users))

    def test_delete_users(self):
        res = client.get(BASE_URL + '/users')
        user_ids = [i["id"] for i in res.get_json().get('data')['users']]
        res = client.delete(BASE_URL + '/users', json={
            'ids': user_ids
        })
        res = client.get(BASE_URL + '/users')
        users = res.get_json().get('data')["users"]
        self.assertEqual(0, len(users))


if __name__ == '__main__':
    tests = [
        testUser('test_create_user_admin'),
        testUser('test_create_user'),
        testUser('test_create_user_again'),
        testUser('test_login_admin'),
        testUser('test_get_user_info'),
        testUser('test_update_user'),
        testUser('test_get_all_users'),
        testUser('test_delete_users')
    ]

    suite = unittest.TestSuite()
    suite.addTests(tests)
    runner = unittest.TextTestRunner()
    runner.run(suite)