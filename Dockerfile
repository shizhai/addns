FROM python:3.11

WORKDIR /

ENV http_proxy=http://192.168.88.87:20172
ENV https_proxy=http://192.168.88.87:20172

RUN apt update
RUN apt install python3.11-dev python3-pip python3-venv -y
RUN pip install --upgrade pip setuptools

RUN mkdir /addns
WORKDIR /addns
COPY addns/ /addns
RUN pip3 install -e .

RUN pip3 install -r requirement.txt

ENV http_proxy=
ENV https_proxy=

ENTRYPOINT ["python3", "/addns/addns.py"]
