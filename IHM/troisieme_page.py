from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage

class Analyse_Review(QDialog):
    def __init__(self, image1_path, image2_path, refs, types):
        super().__init__()

        self.setGeometry(100, 100, 1200, 600)
        self.setWindowTitle("Analysed frames")

        layout = QVBoxLayout()

        # Chargez les images à partir des fichiers PNG
        self.pixmap1 = QPixmap(image1_path)
        self.pixmap2 = QPixmap(image2_path)

        # Créez des QLabel pour afficher les images
        self.label1 = QLabel()
        self.label2 = QLabel()

        # Redimensionnez les images pour qu'elles correspondent à la taille souhaitée
        scaled_pixmap1 = self.pixmap1.scaledToWidth(600)  # Ajustez la largeur selon vos besoins
        scaled_pixmap2 = self.pixmap2.scaledToWidth(600)  # Ajustez la largeur selon vos besoins

        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Affichez les images dans les QLabel
        self.label1.setPixmap(scaled_pixmap1)
        self.label2.setPixmap(scaled_pixmap2)

        # Ajoutez du texte sous chaque image
        self.text_label1 = QLabel("Image 1")
        self.text_label2 = QLabel("Image 2")

        # Définissez la taille de la police pour les textes
        font = self.text_label1.font()
        font.setPointSize(20)  # Ajustez la taille de la police selon vos besoins
        self.text_label1.setFont(font)
        self.text_label2.setFont(font)
        self.text_label1.setStyleSheet("color: orange;")
        self.text_label2.setStyleSheet("color: red;")

        # self.text_label1.setText("Différences entre les références: {}".format(refs))
        self.text_label1.setText(refs)
        self.text_label2.setText("Différences entre les types: {}".format(types))

        # Créez un widget pour contenir les images et le texte
        image_refs_container = QWidget()
        image_ref_layout = QVBoxLayout()
        image_ref_layout.addWidget(self.label1)
        image_ref_layout.addWidget(self.text_label1)
        image_refs_container.setLayout(image_ref_layout)

        image_types_container = QWidget()
        image_types_layout = QVBoxLayout()
        image_types_layout.addWidget(self.label2)
        image_types_layout.addWidget(self.text_label2)
        image_types_container.setLayout(image_types_layout)

        layout_ocr_ia = QHBoxLayout()
        layout_ocr_ia.addWidget(image_refs_container)
        layout_ocr_ia.addWidget(image_types_container)

        layout.addLayout(layout_ocr_ia)
        self.setLayout(layout)
        self.showFullScreen()

class Analyse_Review2(QDialog):
    def __init__(self, image1_path, image2_path):
        super().__init__()

        self.setGeometry(100, 100, 1200, 600)
        self.setWindowTitle("Analysed frames")

        layout = QVBoxLayout()

        # Chargez les images à partir des fichiers PNG
        self.pixmap1 = QPixmap(image1_path)
        self.pixmap2 = QPixmap(image2_path)

        # Créez des QLabel pour afficher les images
        self.label1 = QLabel()
        self.label2 = QLabel()

        # Redimensionnez les images pour qu'elles correspondent à la taille souhaitée
        scaled_pixmap1 = self.pixmap1.scaledToWidth(600)  # Ajustez la largeur selon vos besoins
        scaled_pixmap2 = self.pixmap2.scaledToWidth(600)  # Ajustez la largeur selon vos besoins

        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Affichez les images dans les QLabel
        self.label1.setPixmap(scaled_pixmap1)
        self.label2.setPixmap(scaled_pixmap2)

        self.text_label1 = QLabel(" ⚠️ Ne pas oublier de vérifier la correspondance entre les références et les types !")
        self.text_label1.setStyleSheet("color: orange;")
        font = self.text_label1.font()
        font.setPointSize(25)  # Ajustez la taille de la police selon vos besoins
        self.text_label1.setFont(font)
        self.text_label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Créez un widget pour contenir les images et les textes horizontalement
        images_and_texts_container = QWidget()
        images_and_texts_layout = QHBoxLayout()
        images_and_texts_layout.addWidget(self.label1)
        images_and_texts_layout.addWidget(self.label2)
        images_and_texts_container.setLayout(images_and_texts_layout)

        # Ajoutez les textes sous les images
        layout.addWidget(images_and_texts_container)
        layout.addWidget(self.text_label1)


        self.setLayout(layout)
        self.showFullScreen()