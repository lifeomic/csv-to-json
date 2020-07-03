FROM python:3

WORKDIR /usr/src/app

ENV VIRTUAL_ENV=venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt setup.py ./

RUN pip3 install -r requirements.txt
RUN pip3 install -e .

COPY . .

RUN rm requirements.txt setup.py