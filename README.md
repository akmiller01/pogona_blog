# pogona_blog
Wagtail blog for Pogona

# To run:

docker volume create --name=blogdata
docker-compose build
docker-compose up
docker-compose run web python3 manage.py migrate
docker-compose run web python3 manage.py createsuperuser
docker-compose run web python3 manage.py collectstatic --noinput
