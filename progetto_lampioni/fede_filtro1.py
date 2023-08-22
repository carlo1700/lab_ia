from pprint import pprint
import cv2
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score

def individua_lampioni_colore(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #riscala l'immagine hsv se troppo grande
    if hsv.shape[0] > 1000 or hsv.shape[1] > 1000:
        hsv = cv2.resize(hsv, (int(hsv.shape[1]/2), int(hsv.shape[0]/2)))
    cv2.imshow('hsv', hsv)
    lower_color = np.array([0, 0, 200])
    upper_color = np.array([200, 80, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    #riscala l'immagine mask se troppo grande
    if mask.shape[0] > 1000 or mask.shape[1] > 1000:
        mask = cv2.resize(mask, (int(mask.shape[1]/2), int(mask.shape[0]/2)))
    cv2.imshow('mask', mask)
    kernel = np.ones((12, 12), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return opening

def cerchia(res):
    contours, _ = cv2.findContours(res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtra i contorni per eliminare riflessioni e altre sorgenti luminose
    filtered_contours = []
    for contour in contours:
        # Calcola l'area del contorno
        area = cv2.contourArea(contour)

        if area > 1:
        # Calcola il perimetro del contorno
            perimeter = cv2.arcLength(contour, True)

            # Calcola il rapporto tra area e perimetro
            circularity = 4 * np.pi * area / (perimeter * perimeter)

            # Filtra i contorni in base alla circularità
            if circularity > 0.6:
                filtered_contours.append(contour)

    bounding_boxes = []
    for contour in filtered_contours:
        # Ottieni il bounding box del contorno
        x, y, w, h = cv2.boundingRect(contour)

        # Aggiungi il bounding box alla lista dei bounding box
        bounding_boxes.append((0.0, float(x), float(y), float(w), float(h)))

    # Disegna i contorni filtrati sull'immagine originale
    return cv2.drawContours(image.copy(), filtered_contours, -1, (0, 255, 0), 2), bounding_boxes

def caricafile(file):
    with open(file, 'r') as f:
        res = [tuple(map(float, line.strip().split())) for line in f]
    return res

def foo(file):
    with open(file, 'r') as f:
       res = [1 for line in f]
    return res


# Esempio di utilizzo
image = cv2.imread('roboflow\\test\\images\\immagine_lab_ia-1-_jpg.rf.bbe7082e00bc3ec42ff243f08fd0349b.jpg')
# stampa dimensioni immagine
print(image.shape)

# image = cv2.imread('data/lab2.jpg')
result = individua_lampioni_colore(image)
#riscala l'immagine se troppo grande
if image.shape[0] > 1000 or image.shape[1] > 1000:
    image = cv2.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)))
    result = cv2.resize(result, (int(result.shape[1]/2), int(result.shape[0]/2)))
result, bounding = cerchia(result)
cv2.imshow('Risultato', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(bounding)
pprint(caricafile('roboflow\\test\\\labels\immagine_lab_ia-1-_jpg.rf.bbe7082e00bc3ec42ff243f08fd0349b.txt'))


y_true = foo('roboflow\\test\\labels\\immagine_lab_ia-1-_jpg.rf.bbe7082e00bc3ec42ff243f08fd0349b.txt')
y_pred = [1 for _ in range(len(bounding))]


max_length = max(len(y_true), len(y_pred))

if max_length == len(y_true):
    y_pred += [0] * (max_length - len(y_pred))
else:
    y_true += [0] * (max_length - len(y_true))

pprint(y_true)
pprint(y_pred)

precision = precision_score(y_true, y_pred, average='micro')
print("Precision:", precision)
precision = recall_score(y_true, y_pred, average='micro')
print("recall:", precision)
precision = f1_score(y_true, y_pred, average='micro')
print("f1_score:", precision)
