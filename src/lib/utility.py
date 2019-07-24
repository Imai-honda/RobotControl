# -*- coding: UTF-8 -*-
"""
ヘルパーメソッドをまとめたモジュール
"""


def check_type(parameter, type_group):
    """与えられたパラメータの型が正しいかどうか検証する関数

        Args:
            parameter (str) : 検証対象のパラメータ
            type_group (str) : 想定している型のグループ

        Returns:
            パラメータが想定している型のグループの中にあれば TRUE そうでなければ FALSE

    """

    if type(type_group) == tuple or type(type_group) == list:
        return type(parameter) in type_group

    else:
        return type(parameter) == type_group
