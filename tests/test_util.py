import json
import os
from unittest import TestCase
from unittest.mock import Mock, patch

from requests.exceptions import ConnectionError
from src.http_util import HTTPManager


class TestUtil(TestCase):
    @patch("requests.post")
    def test_success(self, patch_post):
        mock_response = Mock()
        title = "test"
        job_category = "category_1"
        recruit_type = "develop"
        city = "chengdu"
        id = "123"
        mock_response.json.return_value = {
            "data": {
                "job_post_list": [
                    {
                        "id": id,
                        "title": title,
                        "description": "test get from request",
                        "requirement": "",
                        "job_category": {"name": job_category},
                        "recruit_type": {"name": recruit_type},
                        "city_list": [{"name": city}]
                    }
                ]
            }
        }

        mock_response.status_code = 200

        patch_post.return_value = mock_response

        http_manager = HTTPManager()
        http_manager.post('http://localhost', 'test.json')
        with open('test.json', 'r') as fp:
            data = json.load(fp)
            self.assertEqual(data[id]['title'], title)
            self.assertEqual(data[id]['job_category'], job_category)
            self.assertEqual(data[id]['city'], city)

    @patch("requests.post")
    def test_failed(self, patch_post):
        mock_response = Mock()
        mock_response.status_code = 400
        patch_post.return_value = mock_response
        http_manager = HTTPManager()
        http_manager.post('http://localhost', 'test.json')
        self.assertFalse(os.path.exists('test.json'))

    @patch("requests.post")
    def test_error(self, patch_post):
        patch_post.side_effect = ConnectionError()
        with self.assertRaises(ConnectionError):
            http_manager = HTTPManager()
            http_manager.post('http://localhost', 'test.json')

    def tearDown(self):
        """清除测试文件"""
        if os.path.exists('test.json'):
            os.remove('test.json')
