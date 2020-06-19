import PIL
import os
import datetime as dt

from celery.utils.log import get_task_logger

from drf_img_resize import settings
from .celery import app


# Get an instance of a logger
logger = get_task_logger(__name__)


@app.task(bind=True, task_track_started=True)
def resize_img(self, nxt_width, nxt_height, image_path, image_name):
    """
    Resize image in celery task
    """
    size = (nxt_width, nxt_height)
    self.update_state(state='PROGRESS', meta={'progress': 20})
    try:
        # Открываем через PIL наше изображение
        # И выполняем масштабирование
        with PIL.Image.open(image_path) as original_image:
            width, height = original_image.size
            logger.debug(
                f'The original image size is {width} wide x {height} high')
            original_image = original_image.resize(size, PIL.Image.LANCZOS)
            width, height = original_image.size
            logger.debug(
                f'The original image size is {width} wide x {height} high')
            original_image.save(image_path)
            image_url = settings.IMAGES_URL + image_name
            original_image.close()

            logger.info(f'Resize image success: {image_url}')
    except Exception as err:
        image_url = None

        param_list = [f'{key}={value}' for key, value in ({
            'nxt_width': nxt_width,
            'nxt_height': nxt_height,
            'image_path': image_path,
            'image_name': image_name,
            'err': err,
        })]
        log_string = ' '.join(param_list)
        logger.warning(f'fail serializer is error: {log_string}')

    return image_url


@app.task(bind=True)
def cleanup_media_image(self):
    print('================== START TASK ==================')
    all_file = os.listdir(path=settings.IMAGES_ROOT)
    time_now = dt.datetime.now()
    for cur_file in all_file:
        part_name = cur_file.split('.')
        create_time = dt.datetime.fromtimestamp(
            float(f'{part_name[0]}.{part_name[1]}')
        )
        diff_time = time_now - create_time
        if diff_time.days > 0:
            try:
                os.remove(os.path.join(settings.IMAGES_ROOT, cur_file))
            except OSError:
                logger.warning(f'fail deleted file: {cur_file}')
            else:
                logger.info(f'file is deleted: {cur_file}')
