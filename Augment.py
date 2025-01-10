import numpy as np
from PIL import Image, ImageFilter
import ImagesWork as IW

import albumentations as A

def apply_blur(img_path):
    """ Применить Blur """

    image = Image.open(img_path)

    # blurred_image = image.filter(ImageFilter.GaussianBlur(radius=3))

    transform = A.Compose([
        A.GaussianBlur(blur_limit=[11,15], p=1.0)
    ])

    image_np = np.array(image)
    blurred_image = transform(image=image_np)['image']
    blurred_image_pil = Image.fromarray(blurred_image)

    return IW.pil_image_to_qpixmap(blurred_image_pil)


def apply_rotate90(img_path):
    """ Применить вращение на 90 градусов """
    # Ожидаемо, что вращение будет по часовой стрелке, поэтому указываем 270

    image = Image.open(img_path)

    # rotated_image = image.rotate(270)

    transform = A.Compose([
        A.Rotate(limit=[270,270], p=1.0)
    ])

    image_np = np.array(image)
    rotated_image = transform(image=image_np)['image']
    rotated_image_pil = Image.fromarray(rotated_image)

    return IW.pil_image_to_qpixmap(rotated_image_pil)




