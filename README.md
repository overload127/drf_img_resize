# drf_img_resize
create servis and api for resize image


for run celery worker on windows 10
celery -A api_img_resize worker -l info -f logging/celery.log -P eventlet
run for fast test
celery -A api_img_resize worker -l info -P eventlet

for run celery  beat
celery -A api_img_resize beat -l info

(test worked with celery run)

run test all
python manage.py test

run test all
python manage.py test api_img_resize.tests.test_tasks

run all test for coverage
coverage run --source='.' manage.py test api_img_resize

and check coverage reports
coverage report

delete all test stats
coverage erase

show test stats in html
coverage html

AFTER FIRST START
1) create dir:
root/logging
root/media/images
2) python manage.py migrate
