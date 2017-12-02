#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2017/11/28 15:28

import requests
import logging
import time
from bs4 import BeautifulSoup
from http import cookiejar
from selenium import webdriver

# Logging 配置
# 详细日志记录到当前目录下的 op_log 文件中
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='op.log',
                    filemode='w')
# 控制台输出 INFO 级别日志
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(asctime)s: [%(levelname)s]  %(message)s'))
logging.getLogger("").addHandler(console)

# 默认使用 selenium
requests_mode = False
# 新建全局 request
request = requests.session()
# 获取 cookies
request.cookies = cookiejar.LWPCookieJar(filename='cookies')
# 加载 cookies
try:
    request.cookies.load(ignore_discard=True)
except Exception as e:
    logging.warning("No cookie, because %s", e)


# 新建全局 selenium
driver = webdriver.Chrome(executable_path="C:\\Users\\nekuata\\Desktop\\tools\\chromedriver\\chromedriver.exe")


# 自定义 headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Host": "panel.op-net.com",
    "Referer": "https://panel.op-net.com/",
    "Content-type": "application/x-www-form-urlencoded",
    "Connection": "Keep-Alive",
}


def get_email():
    email = input('请输入邮箱: \n')
    return "meowwoolen@gmail.com"


def get_password():
    password = input('请输入密码: \n')
    return "lassock12138"


def get_local():
    local = input('请输入位置编号（默认13；香港：13，日本：14）: \n')
    local = local if local != "" else 13
    return local


def bypass_anti_bot(url, email, password):
    driver.get(url)
    time.sleep(5)
    # time.sleep(3)
    # data_cdn = {
    #     "jschl_vc": driver.find_element_by_name("jschl_vc").get_attribute("value"),
    #     "pass": driver.find_element_by_name("pass").get_attribute("value"),
    #     "jschl_answer": driver.find_element_by_name("jschl_answer").get_attribute("jschl_answer")
    # }
    # url_cdn = driver.find_element_by_id("challenge-form").get_attribute("action")
    # logging.info(url_cdn)
    # response = session.get(url_cdn, data=data_cdn, headers=headers)
    response = driver.page_source
    if email == "" and password == "":
        # 非登陆请求，返回响应内容
        return driver
    if "Can't access your account" in response:
        # logging.info("登录中...")
        # data = {
        #     'email': email,
        #     'password': password
        # }
        # url_login = 'https://panel.op-net.com/login'
        # session.post(url_login, data=data, headers=headers)
        # # 保存cookies
        # session.cookies.save()
        # 此时在登陆界面
        driver.find_element_by_id("email").send_keys(email)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_xpath("//input[@class='button'][@type='submit']").submit()
        # cookies = driver.get_cookies()
        # for cookie in cookies:
        #     request.cookies.set(cookie['name'], cookie['value'])
        #     request.cookies.set_cookie(cookiejar_cookie(cookie))
        #     session.cookies.set(cookie['name'], cookie['value'])
        logging.info("登录成功！")
        # driver.close()
    else:
        logging.info("已登录")


def login(email, password):
    logging.info("检查是否登陆")
    # 提交get请求检查是否已经登录
    url = "https://panel.op-net.com/login"
    driver.get(url)
    response = driver.page_source
    # response = request.get(url, headers=headers)
    if "Can't access your account" in response:
        logging.info("登录中...")
        data = {
            'email': email,
            'password': password
        }
        url = 'https://panel.op-net.com/login'
        request.post(url, data=data, headers=headers)
        # 保存cookies
        request.cookies.save()
        # 如果执行到这里，说明没开anti-bot
        requests_mode = True
    elif "Checking your browser before accessing" in response:
        # 如果启用了anti_bot
        bypass_anti_bot(url, email, password)
    else:
        logging.debug(response)
        logging.info("发生异常，请检查日志")


# 开启requests_mode才需要的东西
def get_token():
    logging.info("初始化...")
    url_cloud = "https://panel.op-net.com/cloud"
    response_vm_id = request.get(url_cloud, headers=headers)
    soup_vm_id = BeautifulSoup(response_vm_id.text, 'lxml')
    try:
        vm_id = soup_vm_id.find('input', attrs={'name': 'vm_id'})['value']
    except Exception as e_vm_id:
        logging.debug(e_vm_id)
        logging.debug(response_vm_id.text)
        exit()
    data = {
        "vm_id": vm_id,
        "x": 20,
        "y": 18
    }
    url_open = "https://panel.op-net.com/cloud/open"
    response_csrf_token = request.post(url_open, data=data, headers=headers)
    soup_csrf_token = BeautifulSoup(response_csrf_token.text, 'lxml')
    csrf_token = soup_csrf_token.find('input', attrs={'name': 'csrf_token'})['value']
    return [csrf_token, vm_id]


def re_create(csrf_token, vm_id, local, flag):
    response_text = ""
    if csrf_token or vm_id:
        # 找不同
        if flag == 1:
            logging.info("The 1st attempt...")
        elif flag == 2:
            logging.info("The 2nd attempt...")
        elif flag == 3:
            logging.info("The 3rd attempt...")
        else:
            logging.info("The %dth attempt...", flag)
        data = {
            "plan": "Plan 01",
            "csrf_token": csrf_token,
            "vm_id": vm_id,
            "location": local,
            "os": "linux-centos-7.1503.01-x86_64-minimal-gen2-v1",
            "hostname": "cat.neko",
            "root": ""
        }
        url = "https://panel.op-net.com/cloud/open"
        response = request.post(url, data=data, headers=headers)
        response_text = response.text
    else:
        driver.find_element_by_xpath("/html/body/div[1]/div[3]/ul[3]/li[1]/a").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[1]/div[2]/table/tbody/tr/td[9]/form/input[2]").click()
    # 判断是否创建成功
    if "Server Creation Progress" in response_text:
        logging.debug(response_text)
        logging.info("嗯？大概是成功了！也有可能是异常？")
        exit()
    else:
        flag += 1
        time.sleep(5)
        re_create(csrf_token, vm_id, flag)


if __name__ == '__main__':
    logging.info("Start")
    login(get_email(), get_password())
    if requests_mode:
        token = get_token()
        if token[0] == "" or token[1] == "":
            logging.error("致命错误！无法获取token")
            exit()
        re_create(token[0], token[1], get_local(), 1)
    else:
        re_create("", "", get_local(), 1)
