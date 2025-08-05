FROM python:3.12-alpine
WORKDIR /code
RUN apk update && apk upgrade
COPY . /code
RUN pip3 install --no-cache-dir -r /code/requirements.txt
CMD python3 aiogram_run.py