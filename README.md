# pogona_blog
Wagtail blog for Pogona

# To run:

docker volume create --name=blogdata
echo "secret_key" > secret_key.txt
docker-compose build
docker-compose up
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
docker-compose run web python manage.py collectstatic --noinput
docker-compose run web python manage.py compress
