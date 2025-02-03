FROM python:3.12
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./mine_shop ./mine_shop

CMD [ "python3", "./mine_shop/manage.py", "runserver", "0.0.0.0:8000" ]