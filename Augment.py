from PIL import Image, ImageFilter
import ImagesWork as IW


def apply_blur(img_path):
    """ Применить Blur """

    image = Image.open(img_path)
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=3))
    return IW.pil_image_to_qpixmap(blurred_image)


def apply_rotate90(img_path):
    """ Применить вращение на 90 градусов """
    # Ожидаемо, что вращение будет по часовой стрелке, поэтому указываем 270

    image = Image.open(img_path)
    rotated_image = image.rotate(270)
    return IW.pil_image_to_qpixmap(rotated_image)




