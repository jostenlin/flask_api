# 基底映像檔 (base image)
FROM python:3.11.4-bookworm

# 安裝 gcsfuse(提供使用 cloud 儲存桶當作本地端檔案系統)
RUN echo "deb http://packages.cloud.google.com/apt gcsfuse-buster main" > /etc/apt/sources.list.d/gcsfuse.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get update && apt-get install -y gcsfuse

# 安裝 pipenv
RUN pip install pipenv

# 安裝依賴
COPY Pipfile Pipfile.lock /
RUN pipenv install --system --deploy

# 建立工作目錄
WORKDIR /app

# 複製應用程式檔案
COPY . /app

# 容器暴露的埠號
# 在Cloud Run中， EXPOSE 命令并不起作用
# EXPOSE 5000

# 一個 Dockerfile 中只能有一個 CMD 指令，CMD 則是在容器運行時所執行的指令。
CMD ["python", "main.py"]
