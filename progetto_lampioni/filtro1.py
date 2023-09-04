from pprint import pprint
import cv2
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score

def individua_lampioni_colore(img):

    # Riduci il rumore dell'immagine con un filtro Gaussiano
    blurred = cv2.GaussianBlur(image, (1, 1), 0)

    _, threshold = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
    #cv2.imshow('threshold', threshold)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening = cv2.morphologyEx(threshold, cv2.MORPH_ERODE, kernel)
    cv2.imshow('opening', opening)

    opening2 = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('opening2', opening2)
    opening3 = cv2.morphologyEx(opening2, cv2.MORPH_TOPHAT, kernel)
    cv2.imshow('opening3', opening3)
    opening4 = cv2.morphologyEx(opening, cv2.MORPH_TOPHAT, kernel)
    cv2.imshow('opening4', opening4)

    res1 = cv2.bitwise_or(opening3, opening4)
    cv2.imshow('res1', res1)

    res1_1 = cv2.bitwise_not(res1)
    cv2.imshow('res1_1', res1_1)


    res2 = cv2.bitwise_and(opening2, opening)
    cv2.imshow('res2', res2)

    res3 = cv2.bitwise_and(res1, res2)
    cv2.imshow('res3', res3)

    res4 = cv2.bitwise_and(res1_1, opening)
    cv2.imshow('res4', res4)

    # solo i bianchi
    lower_white = np.array([200, 200, 200])  # Valori minimi per bianco puro in HSV
    upper_white = np.array([255, 255, 255])  # Valori massimi per bianco puro in HSV

    mask = cv2.inRange(res4, lower_white, upper_white)
    #cv2.imshow('mask', mask)

    res = cv2.bitwise_and(res4, res4, mask=mask)
    cv2.imshow('res', res)

    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    cv2.imshow('res grey', res)

    return res


# bounding_boxes = []

def cerchia(res):
    bounding_boxes = []

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
            if circularity > 0.2:
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
            if distance <= tuple1[3] or distance <= tuple1[4] or distance >= tuple1[3] or distance >= tuple1[4]:
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

def foo(file, bounding_boxes):
    res = find_similar_tuples(caricafile(file), bounding_boxes)
    return res



# Esempio di utilizzo
i = 'roboflow\\test\\images\\immagine_lab_ia-1-_jpg.rf.bbe7082e00bc3ec42ff243f08fd0349b.jpg'
f = 'roboflow\\test\\labels\\immagine_lab_ia-1-_jpg.rf.bbe7082e00bc3ec42ff243f08fd0349b.txt'
image = cv2.imread(i)

result = individua_lampioni_colore(image)
#riscala l'immagine se troppo grande
if image.shape[0] > 1000 or image.shape[1] > 1000:
    image = cv2.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)))
    result = cv2.resize(result, (int(result.shape[1]/2), int(result.shape[0]/2)))
result, bounding_boxes = cerchia(result)
cv2.imshow('Risultato', result)
cv2.waitKey(0)
cv2.destroyAllWindows()


print(bounding_boxes)
pprint(caricafile(f))


y_pred = foo(f, bounding_boxes)
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

