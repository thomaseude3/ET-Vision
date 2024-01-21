from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QWidget
from PyQt6.QtCore import Qt
import sys
import cv2
from ultralytics import YOLO
import shutil

from OCR.programmes.ref_etiquette import OCR_ref_etiquette
from OCR.programmes.type_etiquette import OCR_type_etiquette
from OCR.programmes.ref_produit_blanc import OCR_ref_produit
from OCR.programmes.type_produit_blanc import OCR_type_produit

from IHM.troisieme_page import Analyse_Review
from IHM.comparaison import Comparaison
from OCR.programmes.comparaison_ocr import comparer_listes_refs, comparer_listes_types

from traitement import traitement_etiquette, traitement_produit

# utiliser des QWidgets
# pytoexe

class HomePageLB(QDialog):
    def __init__(self):
        super(HomePageLB, self).__init__()

        self.image_eti_path = "acquisition_image/etiquette_basler.png"
        self.image_prod_path = "acquisition_image/produit_basler.png"
        self.image_prod_binarise = "acquisition_image/produit_basler_binarise.png"

        self.image_eti = cv2.imread(self.image_eti_path)
        self.image_prod = cv2.imread(self.image_prod_path)

        self.diff_ref = []
        self.diff_type = []

        self.comparaison = Comparaison()

        self.initUI()

    def initUI(self):

        self.page = QDialog()
        self.page.setWindowTitle("OCR")
        self.page.setGeometry(200, 200, 300, 200)

        central_widget = QWidget(self)

        # Add a big title label
        big_title_label = QLabel("Sélectionner la zone à lire", self)
        font = big_title_label.font()
        font.setPointSize(24)  # Adjust the font size as needed
        big_title_label.setFont(font)
        big_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_ref_produit = QPushButton('Référence Produit', self)
        self.btn_ref_produit.clicked.connect(self.showRefProduitPage)
        self.btn_ref_produit.setStyleSheet(self.ref_produitStyleSheet())

        self.btn_ref_etiquette = QPushButton('Référence Étiquette', self)
        self.btn_ref_etiquette.clicked.connect(self.showRefEtiquettePage)
        self.btn_ref_etiquette.setStyleSheet(self.ref_etiquetteStyleSheet())

        self.btn_type_produit = QPushButton('Type Produit', self)
        self.btn_type_produit.clicked.connect(self.showTypeProduitPage)
        self.btn_type_produit.setStyleSheet(self.type_produitStyleSheet())

        self.btn_type_etiquette = QPushButton('Type Étiquette', self)
        self.btn_type_etiquette.clicked.connect(self.showTypeEtiquettePage)
        self.btn_type_etiquette.setStyleSheet(self.type_etiquetteStyleSheet())

        btn_retour = QPushButton('Retour', self)
        btn_retour.clicked.connect(self.accept)
        btn_retour.setStyleSheet("""
            background-color: #ff0000;  /* Rouge */
            color: #ffffff;  /* Blanc */
            border: 1px solid #000000;  /* Bordure noire */
            border-radius: 5px;
            padding: 10px;
            font-size: 18px;
            margin: 5px;
            width: 150px;  /* Définir la largeur */
            height: 50px;  /* Définir la hauteur */
                    """)

        self.btn_comparaison = QPushButton('Comparaison', self)
        self.btn_comparaison.clicked.connect(self.traitement_plus_ia_lineaire)
        self.btn_comparaison.setStyleSheet("""
            background-color: #1e90ff;  /* Bleu foncé clair */
            color: #ffffff;  /* Blanc */
            border: 1px solid #000000;  /* Bordure noire */
            border-radius: 5px;
            padding: 10px;
            font-size: 18px;
            margin: 5px;
            width: 150px;  /* Définir la largeur */
            height: 50px;  /* Définir la hauteur */
                """)

        vbox_layout = QVBoxLayout(central_widget)

        # Ajout d'un espace vide au-dessus des boutons
        vbox_layout.addWidget(big_title_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        vbox_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Créer une disposition verticale pour chaque groupe de boutons
        produit_buttons_layout = QVBoxLayout()
        produit_buttons_layout.addWidget(self.btn_ref_produit)
        produit_buttons_layout.addWidget(self.btn_type_produit)
        produit_buttons_layout.addStretch()

        etiquette_buttons_layout = QVBoxLayout()
        etiquette_buttons_layout.addWidget(self.btn_ref_etiquette)
        etiquette_buttons_layout.addWidget(self.btn_type_etiquette)
        etiquette_buttons_layout.addStretch()

        ocr_buttons_layout = QHBoxLayout()
        ocr_buttons_layout.addLayout(produit_buttons_layout)
        ocr_buttons_layout.addLayout(etiquette_buttons_layout)

        vbox_layout.addLayout(ocr_buttons_layout)

        # Ajout d'un espace vide au-dessous des boutons
        vbox_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Ajout du bouton de retour centré en bas de la fenêtre
        vbox_layout.addWidget(btn_retour, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        vbox_layout.addWidget(self.btn_comparaison, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        self.setLayout(vbox_layout)
        self.setWindowTitle('Page d\'Accueil')
        self.setGeometry(100, 100, 400, 300)
        self.showFullScreen()

    def showRefProduitPage(self):
        self.ocr_ref_produit = OCR_ref_produit(self.image_prod, self.image_prod_path)
        self.ocr_ref_produit.new_btn_ref_produit.connect(self.updateButtonStyle_ref_produit)
        self.ocr_ref_produit.exec()

    def showRefEtiquettePage(self):
        self.ocr_ref_etiquette = OCR_ref_etiquette(self.image_eti, self.image_eti_path)
        self.ocr_ref_etiquette.new_btn_ref_eti.connect(self.updateButtonStyle_ref_eti)
        self.ocr_ref_etiquette.exec()

    def showTypeProduitPage(self):
        self.ocr_type_produit = OCR_type_produit(self.image_prod, self.image_prod_path)
        self.ocr_type_produit.new_btn_type_produit.connect(self.updateButtonStyle_type_produit)
        self.ocr_type_produit.exec()

    def showTypeEtiquettePage(self):
        self.ocr_type_etiquette = OCR_type_etiquette(self.image_eti, self.image_eti_path)
        self.ocr_type_etiquette.new_btn_type_eti.connect(self.updateButtonStyle_type_eti)
        self.ocr_type_etiquette.exec()

    def ref_produitStyleSheet(self):
        return """
        background-color: #ffffff;  /* Blanc */
        color: #000000;  /* Noir */
        border: 1px solid #000000;  /* Bordure noire */
        border-radius: 5px;
        padding: 10px;
        font-size: 18px;
        margin: 5px;
    """

    def ref_etiquetteStyleSheet(self):
        return """
        background-color: #ffffff;  /* Blanc */
        color: #000000;  /* Noir */
        border: 1px solid #000000;  /* Bordure noire */
        border-radius: 5px;
        padding: 10px;
        font-size: 18px;
        margin: 5px;
    """

    def type_produitStyleSheet(self):
        return """
        background-color: #ffffff;  /* Blanc */
        color: #000000;  /* Noir */
        border: 1px solid #000000;  /* Bordure noire */
        border-radius: 5px;
        padding: 10px;
        font-size: 18px;
        margin: 5px;
    """

    def type_etiquetteStyleSheet(self):
        return """
        background-color: #ffffff;  /* Blanc */
        color: #000000;  /* Noir */
        border: 1px solid #000000;  /* Bordure noire */
        border-radius: 5px;
        padding: 10px;
        font-size: 18px;
        margin: 5px;
    """

    def updateButtonStyle_ref_produit(self, btn_style):
        sender = self.sender()
        if sender == self.ocr_ref_produit:
            self.btn_ref_produit.setStyleSheet(btn_style)

    def updateButtonStyle_ref_eti(self, btn_style):
        sender = self.sender()
        if sender == self.ocr_ref_etiquette:
            self.btn_ref_etiquette.setStyleSheet(btn_style)

    def updateButtonStyle_type_produit(self, btn_style):
        sender = self.sender()
        if sender == self.ocr_type_produit:
            self.btn_type_produit.setStyleSheet(btn_style)

    def updateButtonStyle_type_eti(self, btn_style):
        sender = self.sender()
        if sender == self.ocr_type_etiquette:
            self.btn_type_etiquette.setStyleSheet(btn_style)

    def traitement_plus_ia_lineaire(self):
        image1 = "images/etiquette_basler_output.png"
        image2 = "images/produit_basler_binarise_output.png"

        self.modele_ia_lineaire()
        self.diff_refs = comparer_listes_refs(self.ocr_ref_etiquette.texte, self.ocr_ref_produit.texte)
        self.diff_type = comparer_listes_types(self.ocr_type_produit.texte, self.ocr_type_etiquette.texte)
        self.show_analysed_images(image1, image2)

    def modele_ia_lineaire(self):
        modele_eti = YOLO("ML_model/modeles_etiquettes/etib.pt")
        modele_prod = YOLO("ML_model/modeles_produits/lineb.pt")
        self.traitement_images()
        self.comparaison.compare_eti(self.image_eti_path, modele_eti)
        self.comparaison.compare_lineaire(self.image_prod_binarise, modele_prod)
        self.comparaison.compare_eti_lineaire()
        self.comparaison.draw_boxes_on_image_lineaire(self.image_prod_binarise,
                                                      self.comparaison.detection_results_lineaires[0])
        self.comparaison.draw_boxes_on_image_etiquette_lineaire(self.image_eti_path,
                                                                self.comparaison.detection_results_etiquettes[0])

        nouveau_dossier = 'acquisition_image/yolo_frames/'
        path1 = "images_ia/predict/etiquette_basler.png"
        path2 = "images_ia/predict2/produit_basler_binarise.png"

        # Déplacer l'image vers le nouveau dossier
        shutil.move(path1, nouveau_dossier + "etiquette_analysee.png")
        shutil.move(path2, nouveau_dossier + "produit_analyse.png")

        # Supprimer le dossier "predict"
        shutil.rmtree("images_ia/predict")
        shutil.rmtree("images_ia/predict2")

    def show_analysed_images(self, image1, image2):
        review_page = Analyse_Review(image1, image2, self.diff_refs, self.diff_type)
        review_page.exec()
        # Ici, vous pouvez ajouter un code pour revenir à la première page après la fermeture de la deuxième page
        if review_page.result() == QDialog.DialogCode.Accepted:
            # Si l'utilisateur a accepté, vous pouvez revenir à la première page
            self.show()

    def traitement_images(self):

        image1_path = "acquisition_image/etiquette_basler.png"
        image2_path = "acquisition_image/produit_basler.png"

        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)

        traitement_etiquette_instance = traitement_etiquette()
        traitement_produit_instance = traitement_produit()

        cleaned_binary_image1 = traitement_etiquette_instance.pre_traitement(image1)
        cleaned_binary_image2 = traitement_produit_instance.pre_traitement(image2)

        binary_image1 = traitement_etiquette_instance.binariser_image(cleaned_binary_image1)
        binary_image2 = traitement_produit_instance.binariser_image(cleaned_binary_image2)

        traitement_etiquette_instance.enregistrer_image(binary_image1, 'etiquette_basler_binarisee.png')
        traitement_etiquette_instance.enregistrer_image(binary_image2, 'produit_basler_binarise.png')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    homepage = HomePageLB()
    sys.exit(app.exec())