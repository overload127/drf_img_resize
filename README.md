# drf_img_resize
create servis and api for resize image


for run celery on windows 10
celery -A api_img_resize worker -l info -f logging/celery.log -P eventlet



API DESCRIPTION

---------------------------------------
Запрос (POST) на создание таска
---------------------------------------
Варианты ответов:
=======================================
# ok
=======================================
status: 'SUCCESS'
task_id: 'xxx'
=======================================
# bad - fail serializer
=======================================
status: 'FAIL'
description: 'fail serializer'
+
field with error
=======================================
# bad - fail serializer
=======================================
status: 'FAIL'
description: 'Can not save the file.Folder "images" is a file type'
---------------------------------------
Запрос (GET) Проверка таска
---------------------------------------
Варианты ответов:
=======================================
# ok
=======================================
status: 'SUCCESS'
task_id: 'xxx'
task_status: 'PADDING|PROCCESS|SUCCESS'
	# PADDING
	proccess: '0'
+++++++++++++++++++++++++++++++++++++++
	# PROCCESS
	proccess: 'x'
+++++++++++++++++++++++++++++++++++++++
	# SUCCESS
	===================================
	# ok
	===================================
	proccess: '100'
	img_url: 'zzz'
	===================================
	# bad
	===================================
	status: 'FAIL'
	description: 'do not have url image'
	proccess: '100'
	img_url: null
=======================================
# bad - task not exist
=======================================
status: 'FAIL'
description: 'task not exist'
=======================================
# bad - other probem
=======================================
status: FAIL
description: 'Unknown error'
task_status: 'task_status'
---------------------------------------
Запрос (GET) удаление таска
---------------------------------------
Варианты ответов:
=======================================
# ok
=======================================
status: 'SUCCESS'
=======================================
# bad - task dos not exist
=======================================
status: 'FAIL'
description: 'task dos not exist'
=======================================
# bad - other probem
=======================================
status: FAIL
description: 'Unknown error'
task_status: 'task_status'
---------------------------------------