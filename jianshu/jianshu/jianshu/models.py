"""
 -*- coding: utf-8 -*-
@File    : models.py
@Time    : 6/19/20 4:49 PM
@Author   : qyf
Connect  : emoqyf@sina.com
@Software: Linux python3.6.8 Django2.0
"""


class ProxyModel:
    def __init__(self, ip):
        self.ip = "http://" + ip

    @property
    def get_ip(self):
        return self.ip
