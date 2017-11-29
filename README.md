### 食用指南

> Base Ubuntu 16.04 64bit

#### 1. 安装Python

咱这个是Python3，请先检查你的Python版本

```shell
python --version
```

如果是Python2，先换成Python3

```shell
rm /usr/bin/python

ln -s /usr/bin/python3.5 /usr/bin/python

python --version
```

#### 2. 安装依赖

Python3自带pip，用pip安装requirements.txt中的依赖

```shell
pip install -r requirements.txt
```

#### 3. 开动了

```shell
python OneProvider.py
```

> Have fun and enjoy it!