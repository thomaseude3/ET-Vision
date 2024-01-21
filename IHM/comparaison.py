from ultralytics import YOLO
import cv2
import os
import time
import datetime

class Comparaison:
    def __init__(self):

        # Résultats de détection
        self.detection_results_etiquettes = []
        self.detected_classes_etiquettes = []

        self.detection_results_lineaires = []
        self.detected_classes_lineaires = []

        self.detection_results_circulaires = []
        self.detected_classes_circulaires = []

        self.classes_manquantes_lineaire = []
        self.classes_supplementaires_lineaire = []

        self.classes_manquantes_circulaire = []
        self.classes_supplementaires_circulaire = []

    def draw_boxes_on_image_circulaire(self, image_path, detections):
        img = cv2.imread(image_path)
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y à %H h %M")

        for detection in detections:
            boxes = detection.boxes.data  # Récupérer les boîtes englobantes
            for box in boxes:
                x1, y1, x2, y2, conf, detected_class = box  # Déballer les valeurs

                if int(detected_class) in self.classes_supplementaires_circulaire[0]:
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 20)  # Couleur bleue pour les classes uniques

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    font_thickness = 1
                    text_color = (255, 255, 255)  # Couleur du texte en blanc
                    text = f"Class: {detected_class}"
                    text_x = int(x1)
                    text_y = int(y1 - 5) if y1 > 20 else int(y2 + 20)

                    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

                if conf < 0.8:
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 5)  # Couleur bleue pour seuil <0.8

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    font_thickness = 1
                    text_color = (255, 255, 255)  # Couleur du texte en blanc
                    text = f"Class: {detected_class}"
                    text_x = int(x1)
                    text_y = int(y1 - 5) if y1 > 20 else int(y2 + 20)

                    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

        output_folder = "images"
        output_folder2 = "/Users/thomaseude/Desktop/dates_photos"
        output_file = os.path.join(output_folder, os.path.basename(image_path).split('.')[0] + '_output.png')
        output_file2 = os.path.join(output_folder2, os.path.basename(image_path).split('.')[0] + f"_le_{timestamp}.png")

        cv2.imwrite(output_file, img)
        cv2.imwrite(output_file2, img)
        print(f"Image avec les boîtes englobantes et classes enregistrée à {output_file}")

    def draw_boxes_on_image_lineaire(self, image_path, detections):
        img = cv2.imread(image_path)
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y à %H h %M")
        for detection in detections:
            boxes = detection.boxes.data  # Récupérer les boîtes englobantes
            for box in boxes:
                x1, y1, x2, y2, conf, detected_class = box  # Déballer les valeurs

                if int(detected_class) in self.classes_supplementaires_lineaire[0]:
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 20)  # Couleur bleue pour les classes uniques

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    font_thickness = 1
                    text_color = (255, 255, 255)  # Couleur du texte en blanc
                    text = f"Class: {detected_class}"
                    text_x = int(x1)
                    text_y = int(y1 - 5) if y1 > 20 else int(y2 + 20)

                    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

                if conf < 0.8:
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 5)  # Couleur bleue pour seuil <0.8

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    font_thickness = 1
                    text_color = (255, 255, 255)  # Couleur du texte en blanc
                    text = f"Class: {detected_class}"
                    text_x = int(x1)
                    text_y = int(y1 - 5) if y1 > 20 else int(y2 + 20)

                    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

        output_folder = "images"
        output_folder2 = "/Users/thomaseude/Desktop/dates_photos"
        output_file = os.path.join(output_folder, os.path.basename(image_path).split('.')[0] + '_output.png')
        output_file2 = os.path.join(output_folder2, os.path.basename(image_path).split('.')[0] + f"_le_{timestamp}.png")

        cv2.imwrite(output_file, img)
        cv2.imwrite(output_file2, img)
        print(f"Image avec les boîtes englobantes et classes enregistrée à {output_file}")

    def draw_boxes_on_image_etiquette_circulaire(self, image_path, detections):
        img = cv2.imread(image_path)
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y à %H h %M")
        for detection in detections:
            boxes = detection.boxes.data  # Récupérer les boîtes englobantes
            for box in boxes:
                x1, y1, x2, y2, conf, detected_class = box  # Déballer les valeurs

                if int(detected_class) in self.classes_manquantes_circulaire[0]:
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 20)  # Couleur bleue pour les classes uniques

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    font_thickness = 1
                    text_color = (255, 255, 255)  # Couleur du texte en blanc
                    text = f"Class: {detected_class}"
                    text_x = int(x1)
                    text_y = int(y1 - 5) if y1 > 20 else int(y2 + 20)

                    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

                if conf < 0.8:
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 5)  # Couleur bleue pour seuil <0.8

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    font_thickness = 1
                    text_color = (255, 255, 255)  # Couleur du texte en blanc
                    text = f"Class: {detected_class}"
                    text_x = int(x1)
                    text_y = int(y1 - 5) if y1 > 20 else int(y2 + 20)

                    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

        output_folder = "images"
        output_folder2 = "/Users/thomaseude/Desktop/dates_photos"
        output_file = os.path.join(output_folder, os.path.basename(image_path).split('.')[0] + '_output.png')
        output_file2 = os.path.join(output_folder2, os.path.basename(image_path).split('.')[0] + f"_le_{timestamp}.png")

        cv2.imwrite(output_file, img)
        cv2.imwrite(output_file2, img)
        print(f"Image avec les boîtes englobantes et classes enregistrée à {output_file}")

    def draw_boxes_on_image_etiquette_lineaire(self, image_path, detections):
        img = cv2.imread(image_path)
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y à %H h %M")

        for detection in detections:
            boxes = detection.boxes.data  # Récupérer les boîtes englobantes
            for box in boxes:
                x1, y1, x2, y2, conf, detected_class = box  # Déballer les valeurs

                if int(detected_class) in self.classes_manquantes_lineaire[0]:
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 20)  # Couleur bleue pour les classes uniques

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    font_thickness = 1
                    text_color = (255, 255, 255)  # Couleur du texte en blanc
                    text = f"Class: {detected_class}"
                    text_x = int(x1)
                    text_y = int(y1 - 5) if y1 > 20 else int(y2 + 20)

                    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

                if conf < 0.8:
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 5)  # Couleur bleue pour seuil <0.8

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    font_thickness = 1
                    text_color = (255, 255, 255)  # Couleur du texte en blanc
                    text = f"Class: {detected_class}"
                    text_x = int(x1)
                    text_y = int(y1 - 5) if y1 > 20 else int(y2 + 20)

                    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

        output_folder = "images"
        output_folder2 = "/Users/thomaseude/Desktop/dates_photos"
        output_file = os.path.join(output_folder, os.path.basename(image_path).split('.')[0] + '_output.png')
        output_file2 = os.path.join(output_folder2, os.path.basename(image_path).split('.')[0] + f" le_{timestamp}.png")

        cv2.imwrite(output_file, img)
        cv2.imwrite(output_file2, img)
        print(f"Image avec les boîtes englobantes et classes enregistrée à {output_file}")

    def compare_eti(self, image_path, model):
        detection_output_eti = model.predict(source=image_path, conf=0.3, save=True, project="images_ia")
        self.detection_results_etiquettes.append(detection_output_eti)

        # Récupérer les classes détectées pour cette image
        classes_detected_etiquettes = set()

        for detection in detection_output_eti:
            boxes = detection.boxes.data
            for box in boxes:
                class_id = int(box[5])
                classes_detected_etiquettes.add(class_id)

        self.detected_classes_etiquettes.append(classes_detected_etiquettes)

    def compare_lineaire(self, image_path, model):
        detection_output_lineaire = model.predict(source=image_path, conf=0.3, save=True, project="images_ia")
        self.detection_results_lineaires.append(detection_output_lineaire)

        # Récupérer les classes détectées pour cette image
        classes_detected_lineaire = set()

        for detection in detection_output_lineaire:
            boxes = detection.boxes.data
            for box in boxes:
                class_id = int(box[5])
                classes_detected_lineaire.add(class_id)

        self.detected_classes_lineaires.append(classes_detected_lineaire)

    def compare_circulaire(self, image_path, model):
        detection_output_circulaire = model.predict(source=image_path, conf=0.3, save=True, project="images_ia")
        self.detection_results_circulaires.append(detection_output_circulaire)

        # Récupérer les classes détectées pour cette image
        classes_detected_circulaire = set()
        for detection in detection_output_circulaire:
            boxes = detection.boxes.data
            for box in boxes:
                class_id = int(box[5])
                classes_detected_circulaire.add(class_id)

        self.detected_classes_circulaires.append(classes_detected_circulaire)

    def compare_eti_lineaire(self):
        self.classes_manquantes_lineaire.append(self.detected_classes_etiquettes[0] -
            self.detected_classes_lineaires[0])

        self.classes_supplementaires_lineaire.append(self.detected_classes_lineaires[0] -
            self.detected_classes_etiquettes[0])

    def compare_eti_circulaire(self):
        self.classes_manquantes_circulaire.append(self.detected_classes_etiquettes[0] -
            self.detected_classes_circulaires[0])

        self.classes_supplementaires_circulaire.append(self.detected_classes_circulaires[0] -
            self.detected_classes_etiquettes[0])