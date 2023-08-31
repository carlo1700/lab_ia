import cv2
import numpy as np

def detect_street_lights(image):

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

    contours, _ = cv2.findContours(res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtra i contorni per eliminare riflessioni e altre sorgenti luminose
    filtered_contours = []
    for contour in contours:
        # Calcola l'area del contorno
        area = cv2.contourArea(contour)

        if area > 0:
        # Calcola il perimetro del contorno
            perimeter = cv2.arcLength(contour, True)

            # Calcola il rapporto tra area e perimetro
            circularity = 4 * np.pi * area / (perimeter * perimeter)

            # Filtra i contorni in base alla circularità
            if circularity > 0.2:
                filtered_contours.append(contour)

    # Disegna i contorni filtrati sull'immagine originale

    return cv2.drawContours(image.copy(), filtered_contours, -1, (0, 255, 0), 2)

# Carica l'immagine di input
input_image = cv2.imread('roboflow\\test\\images\\immagine_lab_ia-12-_jpg.rf.5e1ccebb7aea925338a9418ce2a2f7a2.jpg')
# input_image = cv2.imread('data/lab1.jpg')
# input_image = cv2.imread('data/lab2.jpg')
# input_image = cv2.imread('data/lab3.jpg')
# input_image = cv2.imread('data/lab4.jpg')
# input_image = cv2.imread('data/lab5.jpg')
# input_image = cv2.imread('data/lab6.jpg')

# Individua gli illuminanti stradali
output_image = detect_street_lights(input_image)

cv2.imshow('Output Image', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
