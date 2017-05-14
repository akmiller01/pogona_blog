FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
ADD ./ /src
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 80
CMD gunicorn -w 2 -k gevent -b 0.0.0.0:80 pogona.wsgi
