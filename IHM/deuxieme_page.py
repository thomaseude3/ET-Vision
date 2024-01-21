from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QImage
import os
from PIL import Image
import cv2
import pytesseract
from fuzzywuzzy import fuzz, process
import re
from ultralytics import YOLO
import shutil

from traitement import traitement_etiquette, traitement_produit
from IHM.troisieme_page import Analyse_Review, Analyse_Review2
from IHM.comparaison import Comparaison

from OCR.lineaire.accueil import HomePageL
from OCR.lineaire_blanc.accueil import HomePageLB

class ImageReviewPage(QDialog):
    def __init__(self, image1_path, image2_path):
        super().__init__()

        self.image_eti = "acquisition_image/etiquette_basler.png"
        self.image_produit = "acquisition_image/produit_basler.png"
        self.image_produit_binarise = "acquisition_image/produit_basler_binarise.png"

        self.comparaison = Comparaison()

        self.setGeometry(100, 100, 1200, 600)
        self.setWindowTitle("Examen des images")

        layout = QVBoxLayout()

        # Créez des QLabel pour afficher les images
        self.label1 = QLabel()
        self.label2 = QLabel()

        # Créez des widgets QLabel contenant chacun une image et un layout vertical
        image_widget1 = QWidget()
        image_layout1 = QVBoxLayout()
        image_layout1.addWidget(self.label1)
        image_widget1.setLayout(image_layout1)

        image_widget2 = QWidget()
        image_layout2 = QVBoxLayout()
        image_layout2.addWidget(self.label2)
        image_widget2.setLayout(image_layout2)

        # Créez un widget pour contenir les widgets d'images côte à côte
        image_container = QWidget()
        image_layout = QHBoxLayout()
        image_layout.addWidget(image_widget1)
        image_layout.addWidget(image_widget2)
        image_container.setLayout(image_layout)

        layout.addWidget(image_container)

        # Ajoutez le message et les boutons
        message_label = QLabel(
            "Les photos vous conviennent-elles ? Si oui, sélectionnez le modèle correspondant à la gravure.")
        font = message_label.font()
        font.setPointSize(25)  # Ajustez la taille de la police selon vos préférences
        message_label.setFont(font)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message_label)



        button_layout = QHBoxLayout()
        modele_circulaire = QPushButton("Modèle circulaire")
        modele_circulaire.setStyleSheet("""
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
        modele_circulaire_blanc = QPushButton("Modèle circulaire blanc")
        modele_circulaire_blanc.setStyleSheet("""
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
        modele_lineaire = QPushButton("Modèle linéaire")
        modele_lineaire.setStyleSheet("""
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
        modele_lineaire_blanc = QPushButton("Modèle linéaire blanc")
        modele_lineaire_blanc.setStyleSheet("""
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
        decline_button = QPushButton("Non")
        decline_button.setStyleSheet("""
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
        button_layout.addWidget(modele_lineaire)
        button_layout.addWidget(modele_lineaire_blanc)
        button_layout.addWidget(modele_circulaire)
        button_layout.addWidget(modele_circulaire_blanc)
        button_layout.addWidget(decline_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        modele_lineaire.clicked.connect(self.accueil_lineaire)
        modele_lineaire_blanc.clicked.connect(self.accueil_lineaire_blanc)
        modele_circulaire.clicked.connect(self.traitement_plus_ia_circulaire)
        modele_circulaire_blanc.clicked.connect(self.traitement_plus_ia_circulaire_blanc)
        decline_button.clicked.connect(self.retour_premiere_page)

        # Utilisez le signal showEvent pour obtenir la taille de la fenêtre une fois affichée
        self.showEvent = self.on_show
        self.showFullScreen()

    def on_show(self, event):
        # Obtenez la taille de la fenêtre une fois qu'elle est affichée
        window_size = self.size()
        screen_width = window_size.width()
        screen_height = window_size.height()

        # Redimensionnez les images pour qu'elles correspondent à la moitié de la largeur de la fenêtre
        scaled_pixmap1 = QPixmap(self.image_produit).scaled(screen_width // 2, screen_height,
                                                            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        scaled_pixmap2 = QPixmap(self.image_eti).scaled(screen_width // 2, screen_height,
                                                        aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label1.setPixmap(scaled_pixmap1)

        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setPixmap(scaled_pixmap2)

    def retour_premiere_page(self):
        self.accept()  # Ferme la boîte de dialogue

    def accueil_lineaire(self):
        self.accept()
        homepage = HomePageL()
        homepage.exec()

    def accueil_lineaire_blanc(self):
        self.accept()
        homepage = HomePageLB()
        homepage.exec()

    def show_analysed_images(self, image1, image2):
        review_page = Analyse_Review2(image1, image2)
        review_page.exec()
        # Ici, vous pouvez ajouter un code pour revenir à la première page après la fermeture de la deuxième page
        if review_page.result() == QDialog.DialogCode.Accepted:
            # Si l'utilisateur a accepté, vous pouvez revenir à la première page
            self.show()

    def modele_ia_circulaire(self):
        modele_eti = YOLO("ML_model/modeles_etiquettes/etib.pt")
        modele_prod = YOLO("ML_model/modeles_circulaires/circub.pt")
        self.comparaison.compare_eti(self.image_eti, modele_eti)
        self.comparaison.compare_circulaire(self.image_produit, modele_prod)
        self.comparaison.compare_eti_circulaire()
        self.comparaison.draw_boxes_on_image_circulaire(self.image_produit,
                                                      self.comparaison.detection_results_circulaires[0])
        self.comparaison.draw_boxes_on_image_etiquette_circulaire(self.image_eti,
                                                                self.comparaison.detection_results_etiquettes[0])

        nouveau_dossier = 'acquisition_image/yolo_frames/'
        path1 = "images_ia/predict/etiquette_basler.png"
        path2 = "images_ia/predict2/produit_basler.png"

        # Déplacer l'image vers le nouveau dossier
        shutil.move(path1, nouveau_dossier + "etiquette_analysee.png")
        shutil.move(path2, nouveau_dossier + "produit_analyse.png")

        # Supprimer le dossier "predict"
        shutil.rmtree("images_ia/predict")
        shutil.rmtree("images_ia/predict2")

    def modele_ia_circulaire_blanc(self):
        modele_eti = YOLO("ML_model/modeles_etiquettes/etib.pt")
        modele_prod = YOLO("ML_model/modeles_circulaires/circub.pt")
        self.traitement_images()
        self.comparaison.compare_eti(self.image_eti, modele_eti)
        self.comparaison.compare_circulaire(self.image_produit_binarise, modele_prod)
        self.comparaison.compare_eti_circulaire()
        self.comparaison.draw_boxes_on_image_circulaire(self.image_produit_binarise,
                                                      self.comparaison.detection_results_circulaires[0])
        self.comparaison.draw_boxes_on_image_etiquette_circulaire(self.image_eti,
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

    def traitement_plus_ia_circulaire_blanc(self):
        image1 = "images/etiquette_basler_output.png"
        image2 = "images/produit_basler_binarise_output.png"

        self.modele_ia_circulaire_blanc()
        self.show_analysed_images(image1, image2)

    def traitement_plus_ia_circulaire(self):
        image1 = "images/etiquette_basler_output.png"
        image2 = "images/produit_basler_output.png"

        self.modele_ia_circulaire()
        self.show_analysed_images(image1, image2)