FROM debian:bullseye

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update && apt upgrade -y
RUN apt install -y python3-pip

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT /app/entrypoint.sh
