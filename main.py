# Importations nécessaires
import sys
from PyQt6.QtWidgets import QApplication
from IHM.accueil_ihm import ImageCaptureApp

# Fonction principale
def main():
    # Initialisation de l'application
    app = QApplication(sys.argv)
    # Création de la fenêtre de l'interface graphique
    window = ImageCaptureApp()
    # Affichage de la fenêtre
    window.show()
    # Lancement de la boucle principale de l'application
    sys.exit(app.exec())

# Point d'entrée pour exécuter le script
if __name__ == "__main__":
    main()