# -*- coding: UTF-8 -*-
"""
httpモジュール用のテストモジュール
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import urllib.request
import json
import urllib.error
import sys
from io import StringIO

from protectivestop.sendcommand.src.lib import http


class TestHttp(unittest.TestCase):
    """各テストの初期化と終了処理を指定する基底クラス

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestGetApiCredential(TestHttp):
    """関数get_api_credential用のテストクラス

    """

    def test_normal_input(self):
        """モックを利用して正常な入力に対して適切なAPIクレデンシャル情報を返すか確認するテスト

        """

        with patch("urllib.request.urlopen") as mock_urlopen:
            self.end_point = "https://hogeraas"
            self.account_id = "CI_fuga"
            self.user_name = "hoge"
            self.user_password = "piyopiyo"

            self.mock_response = MagicMock()
            self.response_body = '{"apiKey": "mock_key", ' \
                                 '"token":"mock_token" }'
            self.mock_response.read.return_value.decode.return_value \
                = self.response_body
            self.mock_response.__enter__.return_value = self.mock_response
            mock_urlopen.return_value = self.mock_response

            self.expected_credential = ("mock_key", "mock_token")
            self.unexpected_credential = ("hoge_key", "hoge_token")

            self.assertEqual(self.expected_credential,
                             http.get_api_credential(self.end_point, self.account_id, self.user_name,
                                                     self.user_password))
            self.assertNotEqual(self.unexpected_credential,
                                http.get_api_credential(self.end_point, self.account_id, self.user_name,
                                                        self.user_password))

            self.unpack_args, self.unpack_kwards = mock_urlopen.call_args
            self.mock_request = self.unpack_args[0]

            self.expected_request_url = "{}/user/{}/{}/auth".format(self.end_point, self.account_id, self.user_name)
            self.unexpected_request_url = "{}/user/{}/{}/auth".format("https://pogeraas", "CI_fufu", "huga")

            self.expected_request_data = {"password": self.user_password}
            self.unexpected_request_data = {"pass_word": self.user_password}

            self.expected_request_method = "POST"
            self.unexpected_request_method = "GET"

            self.expected_request_header_content_type = "application/json"
            self.unexpected_request_header_content_type = "text/javascript"

            self.assertEqual(self.expected_request_url, self.mock_request.full_url)
            self.assertNotEqual(self.unexpected_request_url, self.mock_request.full_url)
            self.assertEqual(self.expected_request_data,
                             json.loads(self.mock_request.data.decode("utf-8")))
            self.assertNotEqual(self.unexpected_request_data,
                                json.loads(self.mock_request.data.decode("utf-8")))
            self.assertEqual(self.expected_request_method, self.mock_request.get_method())
            self.assertNotEqual(self.unexpected_request_method, self.mock_request.get_method())
            self.assertEqual(self.expected_request_header_content_type,
                             self.mock_request.get_header('Content-type'))
            self.assertNotEqual(self.unexpected_request_header_content_type,
                                self.mock_request.get_header('Content-type'))

    def test_raise_exception(self):
        """不適切な型を入力した際に例外が発生するか確認するテスト

        """

        self.end_point = 0000
        self.account_id = "CI_fuga"
        self.user_name = "hogehoge"
        self.user_password = "piyopiyo"

        with self.assertRaises(TypeError):
            http.get_api_credential(self.end_point, self.account_id, self.user_name, self.user_password)

        self.end_point = "https://hogeraas.com"
        self.account_id = 0000
        self.user_name = "hogehoge"
        self.user_password = "piyopiyo"

        with self.assertRaises(TypeError):
            http.get_api_credential(self.end_point, self.account_id, self.user_name, self.user_password)

        self.end_point = "https://hogeraas.com"
        self.account_id = "CI_fuga"
        self.user_name = 0000
        self.user_password = "piyopiyo"

        with self.assertRaises(TypeError):
            http.get_api_credential(self.end_point, self.account_id, self.user_name, self.user_password)

        self.end_point = "https://hogeraas.com"
        self.account_id = "CI_fuga"
        self.user_name = "hogehoge"
        self.user_password = 0000

        with self.assertRaises(TypeError):
            http.get_api_credential(self.end_point, self.account_id, self.user_name, self.user_password)

    def test_urlopen_occurs_httperror(self):
        """urllib.request.urlopen()が例外:HTTPErrorを発生した際のアクションが想定通りか確認するテスト

        """
        with patch("urllib.request.urlopen") as mock_urlopen:
            self.end_point = "https://hogeraas.com"
            self.account_id = "CI_fuga"
            self.user_name = "hoge"
            self.user_password = "piyopiyo"

            self.url = ""
            self.expected_code = "503 NG"
            self.unexpected_code = "503 ERROR"
            self.msg = ""
            self.hdrs = ""
            self.open = mock_open()
            self.fp = self.open()

            mock_urlopen.side_effect = urllib.request.HTTPError(self.url, self.expected_code,
                                                                self.msg, self.hdrs, self.fp)

            self.org_stdout, sys.stdout = sys.stdout, StringIO()
            http.get_api_credential(self.end_point, self.account_id, self.user_name, self.user_password)
            self.assertEqual(self.expected_code + "\n", sys.stdout.getvalue())
            self.assertNotEqual(self.unexpected_code + "\n", sys.stdout.getvalue())
            sys.stdout = self.org_stdout

    def test_urlopen_occurs_urlerror(self):
        """urllib.request.urlopen()が例外:URLErrorを発生した際のアクションが想定通りか確認するテスト

        """
        with patch("urllib.request.urlopen") as mock_urlopen:
            self.end_point = "https://hogeraas.com"
            self.account_id = "CI_fuga"
            self.user_name = "hoge"
            self.user_password = "piyopiyo"

            self.expected_reason = "Nothing!!"
            self.unexpected_reason = "Everything!!"

            mock_urlopen.side_effect = urllib.request.URLError(self.expected_reason)

            self.org_stdout, sys.stdout = sys.stdout, StringIO()
            http.get_api_credential(self.end_point, self.account_id, self.user_name, self.user_password)
            self.assertEqual(self.expected_reason + "\n", sys.stdout.getvalue())
            self.assertNotEqual(self.unexpected_reason + "\n", sys.stdout.getvalue())
            sys.stdout = self.org_stdout


class TestGetRobotCredential(TestHttp):
    """関数get_robot_credential用のテストクラス

    """

    def test_normal_input(self):
        """モックを利用して正常な入力に対して適切なロボットクレデンシャル情報を返すか確認するテスト

        """

        with patch("urllib.request.urlopen") as mock_urlopen:
            self.end_point = "https://hogeraas"
            self.api_key = "pukapuka"
            self.token = "dokadoka"

            self.mock_response = MagicMock()
            self.response_body = '{"robotId": "mock_id", ' \
                                 '"secretKey":"mock_key" }'
            self.mock_response.read.return_value.decode.return_value \
                = self.response_body
            self.mock_response.__enter__.return_value = self.mock_response
            mock_urlopen.return_value = self.mock_response

            self.expected_credential = ("mock_id", "mock_key")
            self.unexpected_credential = ("fuga_id", "fuga_key")

            self.assertEqual(self.expected_credential,
                             http.get_robot_credential(self.end_point, self.api_key, self.token))
            self.assertNotEqual(self.unexpected_credential,
                                http.get_robot_credential(self.end_point, self.api_key, self.token))

            self.unpack_args, self.unpack_kwards = mock_urlopen.call_args
            self.mock_request = self.unpack_args[0]

            self.expected_request_url = "{}/robot".format(self.end_point)
            self.unexpected_request_url = "{}/robot".format("https://giko_raas.com")

            self.expected_request_method = "POST"
            self.unexpected_request_method = "GET"

            self.expected_request_header_api_key = self.api_key
            self.unexpected_request_header_api_key = "punipuni"

            self.expected_request_header_token = self.token
            self.unexpected_request_header_token = "bokaboka"

            self.assertEqual(self.expected_request_url, self.mock_request.full_url)
            self.assertNotEqual(self.unexpected_request_url, self.mock_request.full_url)

            self.assertEqual(self.expected_request_method, self.mock_request.get_method())
            self.assertNotEqual(self.unexpected_request_method, self.mock_request.get_method())

            self.assertEqual(self.expected_request_header_api_key,
                             self.mock_request.get_header('X-ciraas-api-key'))
            self.assertNotEqual(self.unexpected_request_header_api_key,
                                self.mock_request.get_header('X-ciraas-api-key'))

            self.assertEqual(self.expected_request_header_token,
                             self.mock_request.get_header('X-ciraas-token'))
            self.assertNotEqual(self.unexpected_request_header_token,
                                self.mock_request.get_header('X-ciraas-token'))

    def test_raise_exception(self):
        """不適切な型を入力した際に例外が発生するか確認するテスト

        """

        self.end_point = 0000
        self.api_key = "fugafuga"
        self.token = "hogehoge"

        with self.assertRaises(TypeError):
            http.get_robot_credential(self.end_point, self.api_key, self.token)


        self.end_point = "https://hogeraas.com"
        self.api_key = 0000
        self.token = "hogehoge"

        with self.assertRaises(TypeError):
            http.get_robot_credential(self.end_point, self.api_key, self.token)

        self.end_point = "https://hogeraas.com"
        self.api_key = "fugafuga"
        self.token = 0000

        with self.assertRaises(TypeError):
            http.get_robot_credential(self.end_point, self.api_key, self.token)


    def test_urlopen_occurs_httperror(self):
        """urllib.request.urlopen()が例外:HTTPErrorを発生した際のアクションが想定通りか確認するテスト

        """
        with patch("urllib.request.urlopen") as mock_urlopen:
            self.end_point = "https://hogeraas.com"
            self.api_key = "fugafuga"
            self.token = "hogehoge"

            self.url = ""
            self.expected_code = "503 NG"
            self.unexpected_code = "503 ERROR"
            self.msg = ""
            self.hdrs = ""
            self.open = mock_open()
            self.fp = self.open()

            mock_urlopen.side_effect = urllib.request.HTTPError(self.url, self.expected_code,
                                                                self.msg, self.hdrs, self.fp)

            self.org_stdout, sys.stdout = sys.stdout, StringIO()
            http.get_robot_credential(self.end_point, self.api_key, self.token)
            self.assertEqual(self.expected_code + "\n", sys.stdout.getvalue())
            self.assertNotEqual(self.unexpected_code + "\n", sys.stdout.getvalue())
            sys.stdout = self.org_stdout

    def test_urlopen_occurs_urlerror(self):
        """urllib.request.urlopen()が例外:URLErrorを発生した際のアクションが想定通りか確認するテスト

        """
        with patch("urllib.request.urlopen") as mock_urlopen:
            self.end_point = "https://hogeraas.com"
            self.api_key = "fugafuga"
            self.token = "hogehoge"

            self.expected_reason = "Nothing!!"
            self.unexpected_reason = "Everything!!"

            mock_urlopen.side_effect = urllib.request.URLError(self.expected_reason)

            self.org_stdout, sys.stdout = sys.stdout, StringIO()
            http.get_robot_credential(self.end_point, self.api_key, self.token)
            self.assertEqual(self.expected_reason + "\n", sys.stdout.getvalue())
            self.assertNotEqual(self.unexpected_reason + "\n", sys.stdout.getvalue())
            sys.stdout = self.org_stdout

class TestAsyncRequest(TestHttp):
    """関数async_request用のテストクラス

    """

    def test_normal_input(self):
        """モックを利用して正常な入力に対して適切なレスポンスを返すか確認するテスト

        """









if __name__ == "__main__":
    unittest.main()
