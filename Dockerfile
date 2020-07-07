FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt setup.py ./

RUN pip3 install -r requirements.txt
RUN pip3 install -e .

COPY . .

RUN rm setup.py requirements.txt