# -*- coding: UTF-8 -*-
"""
HTTP通信に伴う操作をまとめたモジュール
"""

import json
import urllib.request
import urllib.error
import urllib.parse
import traceback
import aiohttp

from ..lib import utility


def get_api_credential(end_point, account_id, user_name, user_password):
    """APIの認証情報(APIキー, トークン)を返す関数

        Args:
            end_point (str) : エンドポイントUR
            account_id (str) : アカウントID
            user_name (str) : ユーザネーム
            user_password (str) : ユーザパスワード

        Returns:
            api_key (str) : APIキー
            token (str) : トークン
    """

    check_list = [
        [end_point, str], [account_id, str], [user_name, str], [user_password, str]
    ]

    for item in check_list:
        if not utility.check_type(item[0], item[1]):
            try:
                raise TypeError
            except TypeError:
                print("Type Error occur in get_api_credential()")
                print(traceback.format_exc())
                raise

    url = "{}/user/{}/{}/auth".format(end_point, account_id, user_name)
    data = {"password": user_password}
    json_data = json.dumps(data).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    method = "POST"

    req = urllib.request.Request(url, data=json_data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as res:
            body = json.loads(res.read().decode())
            return body["apiKey"], body["token"]

    except urllib.error.HTTPError as http_error:
        print(http_error.code)

    except urllib.error.URLError as url_error:
        print(url_error.reason)


def get_robot_credential(end_point, api_key, token):
    """ロボットの認証情報(ロボットIDとシークレットキー)を返す関数

        Args:
            end_point (str) : エンドポイント
            api_key (str) : APIキー
            token (str) : トークン

　　　　　Returns:
            robot_id (str) : ロボットID　
            secret_key (str) : シークレットキー
    """

    check_list = [
        [end_point, str], [api_key, str], [token, str]
    ]

    for item in check_list:
        if not utility.check_type(item[0], item[1]):
            try:
                raise TypeError
            except TypeError:
                print("Type Error occur in get_robot_credential()")
                print(traceback.format_exc())
                raise

    url = "{}/robot".format(end_point)

    headers = {"Content-Type": "application/json",
               "X-ciraas-api-key": api_key,
               "X-ciraas-token": token}

    method = "POST"

    req = urllib.request.Request(url, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as res:
            body = json.loads(res.read().decode())
            return body["robotId"], body["secretKey"]

    except urllib.error.HTTPError as http_error:
        print(http_error.code)

    except urllib.error.URLError as url_error:
        print(url_error.reason)


async def async_request(end_point, robot_id, api_key, token, proxy_url=None):
    """非同期にリクエストを送信する関数

        Args:
            end_point (str) : エンドポイントURL
            robot_id (str) : ロボットID
            api_key (str) : APIキー
            token (str) : トークン
            proxy_url (str) : プロキシURL
    """

    print("Start Request for robot_id:" + robot_id)

    url = "{}/robot/{}/stop".format(end_point, robot_id)
    headers = {
        "Content-Type": "application/json",
        "X-Ciraas-Api-Key": api_key,
        "X-Ciraas-Token": token
    }

    async with aiohttp.ClientSession() as client:
        async with client.put(url, headers=headers, proxy=proxy_url) as response:
            await response.text()
            print("Receive status code:" + str(response.status) + " from robot_id:" + robot_id)
