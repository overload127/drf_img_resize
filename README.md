# drf_img_resize
create servis and api for resize image


for run celery on windows 10
celery -A api_img_resize worker -l info -f logging/celery.log -P eventlet
celery -A api_img_resize worker -l info -P eventlet

run test all
python manage.py test

run test all
python manage.py test

run all test for coverage
coverage run --source='.' manage.py test api_img_resize

and check coverage reports
coverage report
