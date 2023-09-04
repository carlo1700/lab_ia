import cv2
import numpy as np

def detect_street_lights(image):

    # Riduci il rumore dell'immagine con un filtro Gaussiano
    blurred = cv2.GaussianBlur(image, (5, 5), 0)

    # Converti l'immagine in spazio colore HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    cv2.imshow('hsv', hsv)

    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.imshow('img', img)

    _, threshold = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
    cv2.imshow('threshold', threshold)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    cv2.imshow('close', opening)

    # solo i bianchi
    lower_white = np.array([200, 200, 200])  # Valori minimi per bianco puro in HSV
    upper_white = np.array([255, 255, 255])  # Valori massimi per bianco puro in HSV

    mask = cv2.inRange(opening, lower_white, upper_white)
    # cv2.imshow('mask', mask)

    res = cv2.bitwise_or(opening, opening, mask=mask)
    # cv2.imshow('res', res)

    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    cv2.imshow('res grey', res)

    contours, _ = cv2.findContours(res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtra i contorni per eliminare riflessioni e altre sorgenti luminose
    filtered_contours = []
    for contour in contours:
        print(contour)
        # Calcola l'area del contorno
        area = cv2.contourArea(contour)

        if area > 0:
        # Calcola il perimetro del contorno
            perimeter = cv2.arcLength(contour, True)

            # Calcola il rapporto tra area e perimetro
            circularity = 4 * np.pi * area / (perimeter * perimeter)

            # Filtra i contorni in base alla circularità
            if circularity > 0.5:
                filtered_contours.append(contour)

    # Disegna i contorni filtrati sull'immagine originale
    return cv2.drawContours(image.copy(), filtered_contours, -1, (0, 255, 0), 2)

# Carica l'immagine di input
input_image = cv2.imread('lampioni_foto_prof.v1i.yolov8\\train\\images\\lab_ia-17-_jpg.rf.4224789dd1053ccdfaf9d3b45dcc0599.jpg')
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
