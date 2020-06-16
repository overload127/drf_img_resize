import PIL

from drf_img_resize import settings
from drf_img_resize.celery import app


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
            print(f'The original image size is {width} wide x {height} high')
            original_image = original_image.resize(size, PIL.Image.LANCZOS)
            width, height = original_image.size
            print(f'The resized image size is {width} wide x {height} high')
            original_image.save(image_path)
            image_url = settings.IMAGES_URL + image_name
            original_image.close()
    except:
        # в данный момент был случай, когда Image.jpg был Png
        # Добавлю сюда логи
        pass
    return image_url
