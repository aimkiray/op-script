# 食用指南

> Base on Ubuntu 16.04 64bit

## 0. 更新

由于 OneProvider 最近加了 cdn 的 anti-bot，原方案失效，改用 selenium & chrome headless 来替代 requests；requests 仍保留，可自动切换（未测试）

需安装 chrome，版本号大于 59

```shell
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

dpkg -i google-chrome*.deb

apt install -f
```

在这里下载最新版的 [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)（一定要最新版，配合最新版 chrome），解压移动到 PATH 并添加可执行权限

```shell
wget https://chromedriver.storage.googleapis.com/2.33/chromedriver_linux64.zip

unzip chromedriver_linux64.zip

mv ./chromedriver /usr/bin/

chmod 775 /usr/bin/chromedriver
```

## 1. 安装 Python

咱这个是 Python3，请先检查你的Python版本

```shell
python --version
```

如果是 Python2 的话，换成Python3

```shell
add-apt-repository ppa:jonathonf/python-3.6

apt update

apt install python3.6

rm /usr/bin/python

ln -s /usr/bin/python3 /usr/bin/python

python --version
```

若提示 python 未安装，可添加别名或使用 python3

```shell
alias python=/usr/bin/python3
```

## 2. 安装依赖

Python3 自带 pip（大概），用 pip 安装 requirements.txt 中的依赖

```shell
git clone https://github.com/aimkiray/op-script.git

cd op-script

pip3 install -r requirements.txt
```

如果提示`No module named 'pip3'`，需手动安装 pip3

```shell
apt install python3-pip
```

若 pip3 安装 lxml 报错，可尝试

```shell
apt install python3-lxml
```

## 3. 开动了

```shell
python OneProvider.py
```

> Have fun and enjoy it!

> PS. 详细日志见 op.log
