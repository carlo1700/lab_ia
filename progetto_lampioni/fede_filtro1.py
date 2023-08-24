from pprint import pprint
import cv2
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score

def individua_lampioni_colore(img):

    # converte l'immagine in hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #riscala l'immagine hsv se troppo grande
    if hsv.shape[0] > 1000 or hsv.shape[1] > 1000:
        hsv = cv2.resize(hsv, (int(hsv.shape[1]/2), int(hsv.shape[0]/2)))
    cv2.imshow('hsv', hsv)

    #definizione del range di colori da individuare
    lower_color = np.array([0, 0, 200])
    upper_color = np.array([200, 80, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)

    #riscala l'immagine mask se troppo grande
    if mask.shape[0] > 1000 or mask.shape[1] > 1000:
        mask = cv2.resize(mask, (int(mask.shape[1]/2), int(mask.shape[0]/2)))
    cv2.imshow('mask', mask)

    #operazione di erosione per ridurre il rumore
    kernel_erosion = np.ones((4, 4), np.uint8)
    eroded_mask = cv2.erode(mask, kernel_erosion, iterations=1)
    cv2.imshow('eroded_mask', eroded_mask)

    #operazione di dilatazione per ridurre il rumore
    kernel_dilation = np.ones((15, 15), np.uint8)
    dilated_mask = cv2.dilate(eroded_mask, kernel_dilation, iterations=1)
    cv2.imshow('dilated_mask', dilated_mask)


    return dilated_mask


bounding_boxes = []

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

    for contour in filtered_contours:
        # Ottieni il bounding box del contorno
        x, y, w, h = cv2.boundingRect(contour)

        # Aggiungi il bounding box alla lista dei bounding box
        bounding_boxes.append((0.0, float(x)/image.shape[1], float(y)/image.shape[0], float(w)/image.shape[1], float(h)/image.shape[0]))

    # Disegna i contorni filtrati sull'immagine originale
    return cv2.drawContours(image.copy(), filtered_contours, -1, (0, 255, 0), 2), bounding_boxes

def euclidean_distance(tuple1, tuple2):
    return np.sqrt(sum((x - y) ** 2 for x, y in zip(tuple1, tuple2)))

def find_similar_tuples(array1, array2):
    result = []
    for tuple1 in array1:
        found_similar = False
        for tuple2 in array2:
            distance = euclidean_distance(tuple1, tuple2)
            if distance <= tuple1[3] or distance <= tuple1[4]:
                found_similar = True
                array2.remove(tuple2)
                break
        if found_similar:
            result.append(1)
        else:
            result.append(0)
    if(len(array2) > 0):
        result.extend([1] * len(array2))
    return result


def caricafile(file):
    with open(file, 'r') as f:
        res = []
        for line in f:
            elem_riga = line.strip().split()
            tupla = tuple(map(float, elem_riga))
            res.append(tupla)
    return res

def foo(file):
    with open(file, 'r') as f:
       res = find_similar_tuples(caricafile(file), bounding_boxes)
    return res


# Esempio di utilizzo
image = cv2.imread('roboflow\\test\\images\\immagine_lab_ia-11-_jpg.rf.1a5dea0c66e06da0b092d79309fbdb10.jpg')
# stampa dimensioni immagine
print(image.shape)


result = individua_lampioni_colore(image)
#riscala l'immagine se troppo grande
if image.shape[0] > 1000 or image.shape[1] > 1000:
    image = cv2.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)))
    result = cv2.resize(result, (int(result.shape[1]/2), int(result.shape[0]/2)))
result, bounding = cerchia(result)
cv2.imshow('Risultato', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

f = 'roboflow\\test\\labels\\immagine_lab_ia-11-_jpg.rf.1a5dea0c66e06da0b092d79309fbdb10.txt'

print(bounding)
pprint(caricafile(f))


y_pred = foo(f)
y_true = [1 for _ in range(len(caricafile(f)))]


max_length = max(len(y_true), len(y_pred))

if max_length == len(y_true):
    y_pred += [0] * (max_length - len(y_pred))
else:
    y_true += [0] * (max_length - len(y_true))

print("veri")
pprint(y_true)
print("predizione")
pprint(y_pred)

precision = precision_score(y_true, y_pred)
print("Precision:", precision)
precision = recall_score(y_true, y_pred)
print("recall:", precision)
precision = f1_score(y_true, y_pred)
print("f1_score:", precision)
