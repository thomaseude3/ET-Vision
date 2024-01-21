from PyQt6.QtWidgets import QDialog, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsRectItem, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QPen, QImage
from PyQt6.QtCore import Qt, QPointF, pyqtSignal
import pytesseract
import cv2
from PyQt6 import QtCore

class OCR_type_etiquette(QDialog):
    new_btn_type_eti = QtCore.pyqtSignal(str)

    def __init__(self, image1, image1_path):
        super(OCR_type_etiquette, self).__init__()

        self.analysed = None
        self.btn_vert = """
                background-color: #00ff00;  /* Vert */
                color: #000000;  /* Noir */
                border: 1px solid #000000;  /* Bordure noire */
                border-radius: 5px;
                padding: 10px;
                font-size: 18px;
                margin: 5px;"""

        self.btn_rouge = """
                        background-color: #FF0000;  /* Vert */
                        color: #000000;  /* Noir */
                        border: 1px solid #000000;  /* Bordure noire */
                        border-radius: 5px;
                        padding: 10px;
                        font-size: 18px;
                        margin: 5px;"""

        self.texte = []

        self.image1_path = image1_path

        # Convertir l'image NumPy en QImage
        height, width, channel = image1.shape
        bytes_per_line = 3 * width
        self.q_image = QImage(image1.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

        self.pixmap = QPixmap.fromImage(self.q_image)

        # Ajout d'une ligne pour ajuster la taille de l'image à la fenêtre
        self.pixmap = self.pixmap.scaledToWidth(800)  # Ajustez la largeur selon vos besoins

        self.initUI(self.pixmap)

    def initUI(self, image1):
        # Obtenir la taille de la fenêtre
        window_width, window_height = 1200, 500

        # Créer un widget central
        central_widget = QWidget(self)

        # Ajout du titre centré en haut
        title_label = QLabel("Type Étiquette", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        font = title_label.font()
        font.setPointSize(30)  # Ajustez la taille de la police selon vos besoins
        title_label.setFont(font)

        self.view1 = QGraphicsView(self)
        self.scene1 = QGraphicsScene(self)
        self.view1.setScene(self.scene1)

        # Créer des rectangles de sélection pour chaque image
        self.selection_rect1 = QGraphicsRectItem(0, 0, 0, 0)

        # Variable pour indiquer si la souris est enfoncée
        self.mouse_pressed = False

        # Ajouter les images aux QGraphicsScene
        self.image_item1 = self.scene1.addPixmap(self.pixmap)

        # Ajouter un texte au lieu d'un bouton OCR
        ocr_text = QLabel('Sélectionnez la zone à lire', self)
        ocr_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ocr_button = QPushButton('Analyse OCR')
        ocr_button.clicked.connect(self.perform_ocr)
        ocr_button.setStyleSheet("""
                    background-color: #4682B4;  /* Bleu clair */
                    color: #ffffff;  /* Blanc */
                    border: 1px solid #000000;  /* Bordure noire */
                    border-radius: 5px;
                    padding: 15px;  /* Augmenter la taille du padding */
                    font-size: 18px;
                    margin: 5px;
                    width: 200px;  /* Définir la largeur */
                    height: 60px;  /* Définir la hauteur */
                """)

        # Créer un bouton de fermeture
        #close_button = QPushButton('Fermer', self)
        #close_button.clicked.connect(self.accept)

        self.view1.mousePressEvent = lambda event: self.mousePressEvent(event, self.image_item1)
        self.view1.mouseMoveEvent = lambda event: self.mouseMoveEvent(event, self.image_item1)

        # Créer un rectangle de sélection pour l'image 1
        self.selection_rect1 = QGraphicsRectItem(0, 0, 0, 0)

        # Disposition des labels, du texte et du bouton dans une boîte verticale
        vbox = QVBoxLayout(central_widget)
        hbox = QHBoxLayout()

        vbox.addWidget(title_label)  # Ajout du titre centré
        hbox.addWidget(self.view1)
        vbox.addLayout(hbox)
        vbox.addWidget(ocr_text)
        vbox.addWidget(ocr_button)
        #vbox.addWidget(close_button)

        # Définir le layout du widget central
        central_widget.setLayout(vbox)

        # Définir le layout du widget central
        self.setLayout(vbox)

        self.setGeometry(50, 50, window_width, window_height)
        self.setWindowTitle('Fenêtre OCR')
        self.showFullScreen()

    def mousePressEvent(self, event, image_item):
        self.mouse_pressed = True

        # Obtenir les coordonnées de la souris dans la QGraphicsView
        pos = event.pos()
        scene_pos = self.view1.mapToScene(pos)

        # Si c'est le premier clic, créer un nouveau rectangle
        if image_item == self.image_item1 and not self.selection_rect1.scene():
            self.selection_rect1 = QGraphicsRectItem(scene_pos.x(), scene_pos.y(), 0, 0)
            self.selection_rect1.setPen(QPen(Qt.GlobalColor.red))
            self.scene1.addItem(self.selection_rect1)

        # Appeler la méthode de gestion de l'événement
        self.mousePressHandler(event, image_item)

    def mouseMoveEvent(self, event, image_item):
        if self.mouse_pressed:
            self.mousePressHandler(event, image_item)

    def mouseReleaseEvent(self, event):
        if self.mouse_pressed:
            self.mouse_pressed = False
            self.handleMouseRelease()
        super().mouseReleaseEvent(event)

    def handleMouseRelease(self):
        self.perform_ocr()

    def mousePressHandler(self, event, image_item):
        # Obtenir les coordonnées de la souris dans la QGraphicsView
        pos = event.pos()
        scene_pos = self.view1.mapToScene(pos)

        # Mettre à jour les dimensions du rectangle en fonction du mouvement de la souris
        if image_item == self.image_item1:
            self.updateSelectionRect(self.scene1, self.selection_rect1, scene_pos)

        # Sauvegarder la zone sélectionnée dans une image
        self.saveSelectedArea(image_item.pixmap(), self.getSelectionRect(image_item))

    def updateSelectionRect(self, scene, selection_rect, scene_pos):
        if scene.items():
            current_rect = selection_rect.rect()
            width = scene_pos.x() - current_rect.x()
            height = scene_pos.y() - current_rect.y()
            selection_rect.setRect(current_rect.x(), current_rect.y(), width, height)
            scene.update()

    def perform_ocr(self):
        image_eti = cv2.imread("acquisition_image/type_eti.png")

        # Mettre à jour la variable de classe avec le texte extrait
        self.texte.append(pytesseract.image_to_string(image_eti).strip())

        print(self.texte)
        if self.texte == ['']:
            self.new_btn_type_eti.emit(self.btn_rouge)
        else:
            self.new_btn_type_eti.emit(self.btn_vert)
        self.accept()

    def getSelectionRect(self, image_item):
        if image_item == self.image_item1:
            return self.selection_rect1.rect()

    def saveSelectedArea(self, pixmap, rect):
        # Récupérer la zone sélectionnée de l'image
        selected_area = pixmap.copy(rect.toRect())

        # Sauvegarder la zone sélectionnée dans une image
        selected_area.save('acquisition_image/type_eti.png')

    def get_selected_text(self):
        return self.texte_extrait
