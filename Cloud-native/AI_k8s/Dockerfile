# 使用官方 Python 基础镜像
FROM ubuntu:latest

#RUN apt - get update && apt - get install -y python3 python3 - pip
## 设置工作目录
#WORKDIR /app
##WORKDIR D:/app/Anaconda/K-demo1/Cloud-native/AI_k8s
#
## 复制依赖文件并安装依赖
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#
## 复制应用代码
#COPY. /app
#
## 设置环境变量，确保Python脚本使用Python 3
#ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/bin/python3"
## 定义启动命令
#CMD ["python", "app.py"]
FROM centos:8
RUN yum install -y python3 python3-pip

# 设置工作目录
WORKDIR /app

# 更换软件源为阿里云源，加速包下载（Tlinux 可能有不同配置方式）
# 以下是假设的配置示例，根据实际情况调整
RUN sed -i 's/repo.tlinux.com/mirrors.aliyun.com/g' /etc/yum.repos.d/*.repo \
    && yum clean all \
    && yum makecache

# 安装必要的构建工具
RUN yum install -y --nogroups \
        gcc \
        make \
    && yum clean all

# 复制依赖文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . /app

# 设置环境变量，确保 Python 脚本使用 Python 3
# 这一步通常不需要手动设置，Python 镜像已经默认配置
# ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/bin/python3"

# 定义启动命令
CMD ["python", "app.py"]
