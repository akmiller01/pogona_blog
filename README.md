# pogona_blog
Wagtail blog for Pogona

# To run:

docker volume create --name=blogdata
echo "secret_key" > secret_key.txt
docker-compose build
docker-compose up
docker-compose run web python3 manage.py migrate
docker-compose run web python3 manage.py createsuperuser
docker-compose run web python3 manage.py collectstatic --noinput
