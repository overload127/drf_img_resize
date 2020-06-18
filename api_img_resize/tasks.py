import PIL

from drf_img_resize import settings
from .celery import app

from celery.utils.log import get_task_logger

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
