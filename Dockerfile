FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
ADD ./ /src

RUN apt-get update
RUN apt-get -y install cron

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/publish-scheduled-pages
 
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/publish-scheduled-pages

RUN crontab /etc/cron.d/publish-scheduled-pages

WORKDIR /src
RUN pip install -r requirements.txt

CMD service cron start && gunicorn -w 2 -k gevent -b 0.0.0.0:80 pogona.wsgi
