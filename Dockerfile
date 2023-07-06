# 基底映像檔 (base image)
FROM python:3.11.4-bookworm

# 建立工作目錄
WORKDIR /app

# 複製指定的檔案、目錄或遠端檔案 URL，將其加入映像檔檔案系統中的指定位置。
ADD . /app

# 每一個 RUN 指令會在現有映像檔之上加入新的一層
RUN pip install -r requirements.txt 

EXPOSE 8888

# 一個 Dockerfile 中只能有一個 CMD 指令，CMD 則是在容器運行時所執行的指令。
CMD python main.py