#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   : 2017/11/28 15:28
# @Author : aimkiray
# @Email  : root@meowwoo.com

import requests
import logging
from bs4 import BeautifulSoup
from http import cookiejar

# 获取cookies
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies')
# 加载cookies
try:
    session.cookies.load(ignore_discard=True)
except Exception as e:
    logging.warning(e)
    logging.warning("no cookie")

headers = {
    "Content-Length": 0,
    "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cache-Control": "no-cache",
    "Connection": "Keep-Alive",
    "Host": "panel.op-net.com",
    "Referer": "https://panel.op-net.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
    "X-requested-with": "XMLHttpRequest"
}


def get_token():
    url = 'https://panel.op-net.com/cloud'
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_token = soup.find('input', attrs={'name': 'csrf_token'})['value']
    vm_id = soup.find('input', attrs={'name': 'vm_id'})['value']
    return [csrf_token, vm_id]


def get_email():
    return input('请输入邮箱: ')


def get_password():
    return input('请输入密码: ')


def login(your_email, your_password):
    data = {
        'password': your_password,
        'email': your_email
    }
    url = 'https://panel.op-net.com/login'
    session.post(url, data=data, headers=headers)
    # 保存cookies
    session.cookies.save()


def isLogin():
    # 检查是否已经登录
    url = "https://panel.op-net.com/cloud"
    response = session.get(url, headers=headers)
    code = response.status_code
    if code == 200:
        logging.info("登录成功！")
        return True
    else:
        logging.info("登录失败！")
        return False


def re_create(csrf_token, vm_id):
    if not csrf_token or vm_id:
        return
    data = {
        "plan": "Plan 01",
        "csrf_token": csrf_token,
        "vm_id": vm_id,
        "location": 13,
        "os": "linux-centos-7.1503.01-x86_64-minimal-gen2-v1",
        "hostname": "cat.neko",
        "root": ""
    }

    url = "https://panel.op-net.com/cloud/open"
    response = session.post(url, data=data, headers=headers)
    # if response.text.index()


if __name__ == '__main__':
    if isLogin():
        logging.info("登录成功！")
    else:
        email = get_email()
        password = get_password()
        try:
            login(email, password)
        except:
            logging.info("发生异常，重试")
            login(email, password)
    if isLogin():
        logging.info("")
