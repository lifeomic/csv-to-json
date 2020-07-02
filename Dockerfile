FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN make setup-env

COPY . .

CMD [ "python", "./your-daemon-or-script.py" ]