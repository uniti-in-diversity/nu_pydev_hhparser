FROM python:3.7.5-stretch
WORKDIR /app
ADD ./requirements.txt /app
RUN pip install -r requirements.txt
CMD ["uwsgi", "main.ini"]
