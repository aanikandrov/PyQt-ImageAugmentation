from PyQt5.QtGui import QPixmap, QImage
from PIL import Image


def save_qimage(self, qimage, file_path):
    """Сохраняет QImage в указанный файл."""

    if not qimage.save(file_path):
        print("Ошибка при сохранении изображения.")
    else:
        print(f"Изображение успешно сохранено в {file_path}.")


def pil_image_to_qpixmap(pil_image):
    """Конвертирует PIL Image в QPixmap"""

    pil_image = pil_image.convert('RGBA')
    data = pil_image.tobytes("raw", "RGBA")
    qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
    qpixmap = QPixmap.fromImage(qimage)
    return qpixmap


def load_image(path):
    """ Загружает изображение в QPixmap"""

    try:
        image = Image.open(path)
        image = image.convert("RGBA")
        data = image.tobytes("raw", "RGBA")
        qim = QImage(data, image.width, image.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qim)
        return pixmap
    except Exception as e:
        print(f"Error loading image: {e}")
        return QPixmap()  # Возвращаем пустой QPixmap в случае ошибки


def color_for_class(class_id):
    """ Цвет в соответствии с классом для YOLO """

    if class_id == 0:
        s = 'red'
    elif class_id == 1:
        s = 'yellow'
    else:
        s = 'green'
    return s


def text_for_class(class_id):
    """ Подпись в соответствии с классом для YOLO """

    if class_id == 0:
        s = 'fire'
    elif class_id == 1:
        s = 'smoke'
    else:
        s = 'other'
    return s

