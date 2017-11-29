## 食用指南

> Base on Ubuntu 16.04 64bit

### 1. 安装Python

咱这个是Python3，请先检查你的Python版本

```shell
python --version
```

如果是Python2的话，换成Python3

```shell
add-apt-repository ppa:jonathonf/python-3.6

apt update

apt install python3.6

rm /usr/bin/python

ln -s /usr/bin/python3 /usr/bin/python

python --version
```

若提示python未安装，可添加别名或使用python3

```shell
alias python=/usr/bin/python3
```

### 2. 安装依赖

Python3自带pip（大概），用pip安装requirements.txt中的依赖

```shell
git clone https://github.com/aimkiray/op-script.git

cd op-script

pip3 install -r requirements.txt
```

如果提示`No module named 'pip3'`，需安装pip3

```shell
apt install python3-pip
```

若pip3安装lxml报错，可尝试

```shell
apt install python3-lxml
```

### 3. 开动了

```shell
python OneProvider.py
```

> Have fun and enjoy it!

> PS. 详细日志见op.log
