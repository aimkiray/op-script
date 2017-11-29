#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   : 2017/11/28 15:28
# @Author : aimkiray
# @Email  : root@meowwoo.com

import requests
import logging
import time
from bs4 import BeautifulSoup
from http import cookiejar

# Logging配置
# 详细日志记录到当前目录下的op_log文件中
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='op.log',
                    filemode='w')
# 控制台输出INFO级别日志
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(asctime)s: [%(levelname)s]  %(message)s'))
logging.getLogger("").addHandler(console)

# 获取cookies
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies')
# 加载cookies
try:
    session.cookies.load(ignore_discard=True)
except Exception as e:
    logging.warning("No cookie, because %s", e)

# 自定义headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Host": "panel.op-net.com",
    "Referer": "https://panel.op-net.com/",
    "Content-type": "application/x-www-form-urlencoded",
    "Connection": "Keep-Alive",
}


def get_email():
    your_email = input('请输入邮箱: \n')
    return your_email


def get_password():
    your_password = input('请输入密码: \n')
    return your_password


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
    response = session.get(url, headers=headers)
    if "Can't access your account?" in response.text:
        return False
    else:
        return True


def get_token():
    logging.info("初始化...")
    url_cloud = "https://panel.op-net.com/cloud"
    response_vm_id = session.get(url_cloud, headers=headers)
    soup_vm_id = BeautifulSoup(response_vm_id.text, 'lxml')
    vm_id = soup_vm_id.find('input', attrs={'name': 'vm_id'})['value']
    data = {
        "vm_id": vm_id,
        "x": 20,
        "y": 18
    }
    url_open = "https://panel.op-net.com/cloud/open"
    response_csrf_token = session.post(url_open, data=data, headers=headers)
    soup_csrf_token = BeautifulSoup(response_csrf_token.text, 'lxml')
    csrf_token = soup_csrf_token.find('input', attrs={'name': 'csrf_token'})['value']
    return [csrf_token, vm_id]


def re_create(csrf_token, vm_id, flag):
    if csrf_token == "" or vm_id == "":
        logging.error("致命错误！无法获取token")
        exit()
    logging.info("第 %d 次尝试", flag)
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
    if "The requested location is currently unavailable" in response.text or \
       "it is currently impossible" in response.text:
        flag += 1
        time.sleep(5)
        re_create(csrf_token, vm_id, flag)
    else:
        logging.info("创建成功！")
        exit()


if __name__ == '__main__':
    logging.info("Start")
    if isLogin():
        logging.info("登录成功！")
    else:
        login(get_email(), get_password())
        logging.info("登录成功！")
    token = get_token()
    re_create(token[0], token[1], 1)
