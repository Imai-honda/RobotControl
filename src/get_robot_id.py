# -*- coding: utf-8 -*-
"""
ロボットIDを取得するスクリプト
"""

from .lib import http

if __name__ == '__main__':

    END_POINT = 'https://api.t360.raasdev.io'
    ACCOUNT_ID = 'CI0001'
    USER_NAME = 'admin'
    USER_PASSWORD = 'b8eN3g)g/HhY'

    api_key, token = http.get_api_credential(END_POINT, ACCOUNT_ID, USER_NAME, USER_PASSWORD)
    robot_id, secret_key = http.get_robot_credential(END_POINT, api_key, token)

    print("robot_id:" + robot_id)