
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QDialog, QGridLayout, QGraphicsScene, QGraphicsView

from PIL import Image, ImageDraw, ImageFont

from PyQt5.QtGui import QPixmap, QImage
from PIL import Image

import shutil

import FileWork
import ImagesWork
import Augment


class ImageWindow(QDialog):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 650, 400)
        self.setFixedSize(650, 400)

        self.augmentations_scrollArea = QtWidgets.QScrollArea(self)
        self.augmentations_scrollArea.setGeometry(QtCore.QRect(380, 60, 221, 281))
        self.augmentations_scrollArea.setWidgetResizable(True)
        self.augmentations_scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(380, 60, 221, 281))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.augmentations_scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.augmentations_layout = QGridLayout()
        self.augmentations_container = QWidget()
        self.augmentations_container.setLayout(self.augmentations_layout)
        self.augmentations_scrollArea.setWidget(self.augmentations_container)

        self.push_close = QtWidgets.QPushButton('Close', self)
        self.push_close.setGeometry(QtCore.QRect(520, 350, 50, 23))
        self.push_close.setObjectName("push_close")

        self.push_save = QtWidgets.QPushButton('Save', self)
        self.push_save.setGeometry(QtCore.QRect(450, 350, 50, 23))
        self.push_save.setObjectName("push_save")

        self.push_YOLO = QtWidgets.QPushButton('YOLO', self)
        self.push_YOLO.setGeometry(QtCore.QRect(380, 350, 50, 23))
        self.push_YOLO.setObjectName("push_YOLO")

        self.push_zoomIN = QtWidgets.QPushButton('+', self)
        self.push_zoomIN.setGeometry(QtCore.QRect(20, 370, 50, 23))
        self.push_zoomIN.setObjectName("push_zoomIN")

        self.push_zoomOUT = QtWidgets.QPushButton('-', self)
        self.push_zoomOUT.setGeometry(QtCore.QRect(80, 370, 50, 23))
        self.push_zoomOUT.setObjectName("push_zoomOUT")

        self.push_zoomRESET = QtWidgets.QPushButton('0', self)
        self.push_zoomRESET.setGeometry(QtCore.QRect(140, 370, 50, 23))
        self.push_zoomRESET.setObjectName("push_zoomRESET")

        self.check_blur = QtWidgets.QCheckBox('Blur', self)
        self.check_blur.setGeometry(QtCore.QRect(380, 30, 70, 20))
        self.check_blur.setObjectName("check_blur")

        self.check_rotate90 = QtWidgets.QCheckBox('Rotate90', self)
        self.check_rotate90.setGeometry(QtCore.QRect(500, 30, 70, 20))
        self.check_rotate90.setObjectName("check_rotate90")

        self.label_imageName = QtWidgets.QLabel('image', self)
        self.label_imageName.setGeometry(QtCore.QRect(20, 2, 600, 20))
        self.label_imageName.setObjectName("label_imageName")

        # Подключение функционала
        self.ImageWindow_functional(image_path)

        self.pixmap = ImagesWork.load_image(self.path)
        self.scene = QGraphicsScene(self)
        self.scene.addPixmap(self.pixmap)

        self.graphics_view = QGraphicsView(self)
        self.graphics_view.scale(self.scale_factor, self.scale_factor)
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setGeometry(20, 20, 350, 350)

    def ImageWindow_functional(self, image_path):
        """ Функционал """

        self.scale_factor = 0.54
        self.isYOLO = False
        self.path = image_path

        self.makeYOLO()

        self.label_imageName.setText(self.path)

        self.check_blur.stateChanged.connect(self.add_blur)
        self.check_rotate90.stateChanged.connect(self.add_rotate90)

        self.push_save.clicked.connect(self.create_augmentations)
        self.push_close.clicked.connect(self.close)
        self.push_YOLO.clicked.connect(self.change_image_to_YOLO)

        self.push_zoomOUT.clicked.connect(self.zoomOUT)
        self.push_zoomIN.clicked.connect(self.zoomIN)
        self.push_zoomRESET.clicked.connect(self.zoomRESET)



    def create_augmentations(self):
        """ Сохраняет выбранные аугментации перед закрытием окна """

        if self.check_blur.isChecked():
            new_image = QPixmap(Augment.apply_blur(self.path))
            new_image_path = FileWork.find_dot_index(self.path) + "_blur.jpg"

            new_image.save(new_image_path, "png")

            old_label_path = FileWork.labels_filepath(self.path)
            index = old_label_path.rfind('.txt')
            new_label_path = old_label_path[:index] + '_blur' + '.txt'
            shutil.copy(old_label_path, new_label_path)

        if self.check_rotate90.isChecked():
            new_image = QPixmap(Augment.apply_rotate90(self.path))
            new_image_path = FileWork.find_dot_index(self.path) + "_rotate90.jpg"

            new_image.save(new_image_path, "png")

            old_label_path = FileWork.labels_filepath(self.path)
            index = old_label_path.rfind('.txt')
            new_label_path = old_label_path[:index] + '_rotate90' + '.txt'
            shutil.copy(old_label_path, new_label_path)
            # Копируем, а потом уже будем менять координаты
            self.create_annotation_for_Rotate90(new_label_path)

        self.close()


    def zoomIN(self):
        """ Приблизить """

        if self.scale_factor < 3.0:
            self.graphics_view.scale(1.2, 1.2)
            self.scale_factor *= 1.2

    def zoomOUT(self):
        """ Отдалить  """

        if self.scale_factor > 0.54:
            self.graphics_view.scale(1 / 1.2, 1 / 1.2)
            self.scale_factor /= 1.2

    def zoomRESET(self):
        """ Восстановить изначальный масштаб """

        self.scale_factor = 0.54
        self.graphics_view.resetTransform()
        self.graphics_view.scale(self.scale_factor, self.scale_factor)

    def change_image_to_YOLO(self):
        """ Включает/отключает отображение масок """

        if self.isYOLO:
            self.scene = QGraphicsScene(self)
            self.scene.addPixmap(self.pixmap)
            self.graphics_view.setScene(self.scene)
            self.isYOLO = False
        else:
            self.scene = QGraphicsScene(self)
            self.scene.addPixmap(self.pixmap_YOLO)
            self.graphics_view.setScene(self.scene)
            self.isYOLO = True


    def create_annotation_for_Rotate90(self, path):
        """ Создаёт аннотацию для полученного после Rotate90 изображения """

        with open(path, 'r') as f:
            annotations = f.readlines()

        with open(path, 'w') as f:
            for annotation in annotations:
                class_id, x_center, y_center, width, height = map(float, annotation.strip().split())
                f.write(f"{int(class_id)} {1 - y_center} {x_center} {height} {width}\n")


    def makeYOLO(self):
        """ Читает аннотации и рисуем на pixmap """

        new_path = FileWork.labels_filepath(self.path)
        with open(new_path, 'r') as f:
            annotations = f.readlines()

        image = Image.open(self.path).convert("RGB")
        h, w = image.size

        for annotation in annotations:
            class_id, x_center, y_center, width, height = map(float, annotation.strip().split())

            x_center *= w
            y_center *= h
            width *= w
            height *= h

            x1 = float(x_center - width / 2)
            y1 = float(y_center - height / 2)
            x2 = float(x_center + width / 2)
            y2 = float(y_center + height / 2)

            top_left = (x1, y1)
            bottom_right = (x2, y2)

            draw = ImageDraw.Draw(image)
            color = ImagesWork.color_for_class(class_id)
            draw.rectangle((top_left, bottom_right), outline=color, width=6)

            text = ImagesWork.text_for_class(class_id)
            text_position = (top_left[0], top_left[1] - 20)
            font = ImageFont.load_default()
            draw.text(text_position, text, fill=color, font=font)

        image = image.convert("RGBA")
        data = image.tobytes("raw", "RGBA")
        qim = QImage(data, image.width, image.height, QImage.Format_RGBA8888)
        pix = QPixmap.fromImage(qim)

        self.pixmap_YOLO = pix

    def add_blur(self):
        """ Добавляет Blur в предпросмотр аннотаций """

        if self.check_blur.isChecked():
            self.blur_caption = QLabel("Blur")
            self.augmentations_layout.addWidget(self.blur_caption)
            self.blur_label = QLabel()
            pix = QPixmap(Augment.apply_blur(self.path))
            self.blur_label.setPixmap(pix.scaled(150, 150, Qt.KeepAspectRatio))
            self.augmentations_layout.addWidget(self.blur_label)
        else:
            self.augmentations_layout.removeWidget(self.blur_caption)
            self.blur_caption = ""
            self.augmentations_layout.removeWidget(self.blur_label)
            self.blur_label = ""

    def add_rotate90(self):
        """ Добавляет Rotate90 в предпросмотр аннотаций """

        if self.check_rotate90.isChecked():
            self.rotate_caption = QLabel("Rotate 90")
            self.augmentations_layout.addWidget(self.rotate_caption)
            self.rotate_label = QLabel()
            pix = QPixmap(Augment.apply_rotate90(self.path))
            self.rotate_label.setPixmap(pix.scaled(150, 150, Qt.KeepAspectRatio))
            self.augmentations_layout.addWidget(self.rotate_label)
        else:
            self.augmentations_layout.removeWidget(self.rotate_caption)
            self.rotate_caption = ""
            self.augmentations_layout.removeWidget(self.rotate_label)
            self.rotate_label = ""



