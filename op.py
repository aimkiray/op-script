#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2017/11/28 15:28
from functools import wraps

import requests
import logging
import time
from bs4 import BeautifulSoup
from http import cookiejar
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

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
# 新建 requests
request = requests.session()

# 配置 chrome headless 模式
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")
# 新建全局 selenium
browser = webdriver.Chrome(chrome_options=chrome_options)
# 最长等待 120s
browser.implicitly_wait(120)
# 抄起 jQuery 就是干 XD（形势所迫）
jquery = open("jquery-3.2.1.min.js", "r").read()

# 自定义 header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Host": "panel.op-net.com",
    "Referer": "https://panel.op-net.com/",
    "Content-type": "application/x-www-form-urlencoded",
    "Connection": "Keep-Alive"
}


def get_email():
    while True:
        email = input('请输入邮箱: \n')
        if email:
            break
    return email


def get_password():
    while True:
        password = input('请输入密码: \n')
        if password:
            break
    return password


def get_local():
    local = input('请输入位置编号（默认13；香港：13，日本：14）: \n')
    local = local if local != "" else 13
    return local


def bypass_anti_bot(url, email, password):
    browser.get(url)
    # 检查界面是否加载完毕
    locator = (By.XPATH, '''/html/body/div[1]/div[2]/div[1]/form/ul/li[3]/input''')
    WebDriverWait(browser, 100, 0.5).until(ec.presence_of_element_located(locator))
    response_text = browser.page_source
    if email == "" and password == "":
        # 非登陆请求，返回响应内容
        return browser
    if "Can't access your account" in response_text:
        # 此时在登陆界面
        browser.find_element_by_id("email").send_keys(email)
        browser.find_element_by_id("password").send_keys(password)
        browser.find_element_by_xpath("//input[@class='button'][@type='submit']").submit()
        logging.info("登录成功！")
    else:
        logging.info("已登录")


def login(email, password):
    logging.info("检查是否登陆")
    # 提交get请求检查是否已经登录
    url = "https://panel.op-net.com/login"
    browser.get(url)
    response = browser.page_source
    # response = request.get(url, headers=headers)
    if "Can't access your account" in response:
        # 获取 cookies
        request.cookies = cookiejar.LWPCookieJar(filename='cookies')
        # 加载 cookies
        try:
            request.cookies.load(ignore_discard=True)
        except Exception as e:
            logging.warning("No cookie, because %s", e)
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
        global requests_mode
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
    vm_id = soup_vm_id.find('input', attrs={'name': 'vm_id'})['value']
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


def get_token_selenium():
    browser.find_element_by_xpath("/html/body/div[1]/div[3]/ul[3]/li[1]/a").click()
    vm_id = browser.find_element_by_name("vm_id").get_attribute("value")
    form_vm = '''
    var form = $("<form></form>");
    form.attr('action', '/cloud/open');
    form.attr('method', 'post');
    var params = {
        "vm_id": %s,
        "x": 11,
        "y": 11
    };
    for (var key in params) {
        var input = $("<input type='hidden' name='" + key + "' />");
        input.attr('value', params[key]);
        form.append(input);
    }
    form.appendTo("body");
    form.css('display', 'none');
    form.submit();''' % vm_id
    # form_vm = form_vm.replace(" ", "").replace("\n", "")
    # 检查界面是否加载完毕
    locator = (By.ID, 'th1')
    WebDriverWait(browser, 100, 0.5).until(ec.presence_of_element_located(locator))
    browser.execute_script(jquery)
    browser.execute_script(form_vm)
    # 检查界面是否加载完毕
    locator = (By.ID, 'chkLoc_19')
    WebDriverWait(browser, 100, 0.5).until(ec.presence_of_element_located(locator))
    csrf_token = browser.find_element_by_name("csrf_token").get_attribute("value")
    return [csrf_token, vm_id]


def create_loop(csrf_token, vm_id, local, flag):
    global requests_mode
    while True:
        # 找不同（计数）
        if flag == 1:
            logging.info("The 1st attempt...")
        elif flag == 2:
            logging.info("The 2nd attempt...")
        elif flag == 3:
            logging.info("The 3rd attempt...")
        else:
            logging.info("The %dth attempt...", flag)
        if requests_mode:
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
            if csrf_token == "" or vm_id == "":
                token_selenium = get_token_selenium()
                if token_selenium[0] == "" or token_selenium[1] == "":
                    logging.error("致命错误！无法获取 token")
                    # 关闭 chrome
                    browser.close()
                    exit()
                else:
                    csrf_token = token_selenium[0]
                    vm_id = token_selenium[1]
            form_buy = '''
            var form = $("<form></form>");
            form.attr('action', '/cloud/open');
            form.attr('method', 'post');
            form.attr('onsubmit', 'ShowLoading()');
            var params = {
                "plan": "Plan 01",
                "csrf_token": "%s",
                "vm_id": %s,
                "location": %s,
                "os": "linux-centos-7.1503.01-x86_64-minimal-gen2-v1",
                "hostname": "cat.neko",
                "root": ""
            };
            for (var key in params) {
                var input = $("<input type='hidden' name='" + key + "' />");
                input.attr('value', params[key]);
                form.append(input);
            }
            form.appendTo("body");
            form.css('display', 'none');
            form.submit();''' % (csrf_token, vm_id, local)
            # form_buy = form_buy.replace(" ", "").replace("\n", "")
            browser.execute_script(jquery)
            browser.execute_script(form_buy)
            # 检查界面是否加载完毕
            locator_re = (By.XPATH, '''//*[@id="btnSumbit"]''')
            # locator_else = (By.XPATH, '''''')  TODO 创建成功的情况（咱还没见过呢(┬＿┬)）
            try:
                WebDriverWait(browser, 100, 0.5).until(ec.presence_of_element_located(locator_re))
            except Exception as timeout:
                # 可能是超时或成功，继续判断
                logging.debug(timeout)
            response_text = browser.page_source
        # 判断是否创建成功
        if "Server Creation Progress" in response_text:
            logging.debug(response_text)
            logging.info("咦？好像成功了！")
            # 关闭 chrome
            browser.close()
            exit()
        else:
            flag += 1
            # +3s提交一次
            time.sleep(3)
            # return [csrf_token, vm_id, local, flag]
            # re_create(csrf_token, vm_id, local, flag)


# def cache_loop(fn):
#     cache = {}
#     miss = object()
#
#     @wraps(fn)
#     def wrapper(*args):
#         result = cache.get(args, miss)
#         if result is miss:
#             result = fn(*args)
#             cache[args] = result
#         return result
#
#     return wrapper


if __name__ == '__main__':
    logging.info("Start")
    time.sleep(0.1)
    login(get_email(), get_password())
    if requests_mode:
        # 如果没开 anti-bot，则不需要 js 环境
        time.sleep(0.1)
        token = get_token()
        if token[0] == "" or token[1] == "":
            logging.error("致命错误！无法获取 token")
            exit()
        create_loop(token[0], token[1], get_local(), 1)
    else:
        create_loop("", "", get_local(), 1)
