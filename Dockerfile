FROM debian:bullseye

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update && apt upgrade -y
RUN apt install -y python3-pip
RUN pip config set global.index-url https://mirror.sjtu.edu.cn/pypi/web/simple

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT /app/entrypoint.sh
