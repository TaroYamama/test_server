# Dockerfile (修复版)

# 1. 选择一个支持多平台 (包括 arm64) 的 Python 官方基础镜像
FROM python:3.11-slim

# 2. 设置容器内的工作目录
WORKDIR /app

# 3. (再次更新) 安装所有编译依赖
#    - build-essential: 提供 C/C++ 编译器和链接器 (gcc/cc)。
#    - pkg-config:      让编译脚本能找到其他库的工具。
#    - libssl-dev:      OpenSSL 的开发文件，供需要加密功能的库编译时使用。
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libssl-dev && \
    rm -rf /var/lib/apt/lists/*
# 4. 复制依赖文件到工作目录
COPY requirements.txt .

# 5. 安装 Python 依赖
#    现在因为系统里已经有了编译工具，这一步应该可以成功了
RUN pip install --no-cache-dir -r requirements.txt

# 6. 复制应用程序代码到工作目录
COPY server.py .
COPY models/ ./models/
# 7. 声明容器对外暴露的端口
EXPOSE 59590

# 8. 定义容器启动时执行的命令
CMD ["python", "server.py"]
