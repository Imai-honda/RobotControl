# -*- coding: utf-8 -*-
"""
複数台のロボットに対して非同期にhttpリクエストを行い同時に停止信号を送るスクリプト
"""

import asyncio

from .lib import http


if __name__ == '__main__':

    END_POINT = 'https://api.t360.raasdev.io'
    ACCOUNT_ID = 'CI0001'
    USER_NAME = 'admin'
    USER_PASSWORD = 'b8eN3g)g/HhY'

    robot_ids = [
         'aee4a0c4-70b9-46bd-b471-54cde49adaee',
         '0c809444-3104-439c-b1ca-67572ccd0a20'
    ]

    proxy_url = 'http://localhost:3128'

    api_key, token = http.get_api_credential(END_POINT, ACCOUNT_ID, USER_NAME, USER_PASSWORD)

    reqs = [http.async_request(END_POINT, robot_id, api_key, token, proxy_url=proxy_url) for robot_id in robot_ids]

    wait = asyncio.wait(reqs)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(wait)
