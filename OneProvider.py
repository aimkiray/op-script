#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   : 2017/11/28 15:28
# @Author : aimkiray
# @Email  : root@meowwoo.com

import requests
import logging
from bs4 import BeautifulSoup
from http import cookiejar

logging.basicConfig(level=logging.INFO)
# 获取cookies
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies')
# 加载cookies
try:
    session.cookies.load(ignore_discard=True)
except Exception as e:
    logging.warning("No cookie, because %s", e)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Host": "panel.op-net.com",
    "Referer": "https://panel.op-net.com/",
    "Content-type": "application/x-www-form-urlencoded",
    "Connection": "Keep-Alive",
}


def get_token():
    url = 'https://panel.op-net.com/cloud'
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_token = soup.find('input', attrs={'name': 'csrf_token'})['value']
    vm_id = soup.find('input', attrs={'name': 'vm_id'})['value']
    return [csrf_token, vm_id]


def get_email():
    return input('请输入邮箱: \n')


def get_password():
    return input('请输入密码: \n')


def login(your_email, your_password):
    logging.info("登录中...")
    data = {
        'email': your_email,
        'password': your_password
    }
    url = 'https://panel.op-net.com/login'
    try:
        session.post(url, data=data, headers=headers)
    except Exception as e:
        logging.info("Exception %s, reTry.", e)
        login(your_email, your_password)
        return
    # 保存cookies
    session.cookies.save()


def isLogin():
    logging.info("检查是否登陆")
    # 检查是否已经登录
    url = "https://panel.op-net.com/cloud"
    response = session.get(url, headers=headers, allow_redirects=False)
    if "Can't access your account?" in response.text:
        logging.info("没有登陆")
        return False
    else:
        return True


def re_create(csrf_token, vm_id):
    if not csrf_token or vm_id:
        logging.error("致命错误！无法获取csrf")
        exit()
    logging.info("尝试创建")
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
    logging.info("start")
    if isLogin():
        logging.info("登录成功！")
    else:
        email = get_email()
        password = get_password()
        login(email, password)
    if isLogin():
        logging.info("登录成功！")
        # token = get_token()
        # re_create(token[0], token[1])
