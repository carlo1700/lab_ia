import cv2
import numpy as np

# Funzione per l'individuazione degli illuminanti
def individua_illuminanti_immagine(image):
    # Converte l'immagine in scala di grigi
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)


    # Applica una soglia per estrarre i punti di luce
    _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    cv2.imshow('threshold', threshold)

    # Applica un filtro per rimuovere il rumore di fondo
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    cv2.imshow('opening', opening)

    # Trova le componenti connesse
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    illuminanti = []

    # Filtra le regioni connesse per mantenere solo gli illuminanti desiderati
    for contour in contours:
        # Calcola l'area del contorno
        area = cv2.contourArea(contour)

        # Filtra i falsi positivi in base all'area
        if area > 10 and area < 5000:
            # Calcola il centroide del contorno
            moments = cv2.moments(contour)
            centroid_x = int(moments['m10'] / moments['m00'])
            centroid_y = int(moments['m01'] / moments['m00'])

            # Aggiungi il centroide agli illuminanti individuati
            illuminanti.append((centroid_x, centroid_y))

    return illuminanti

# Carica l'immagine
# image = cv2.imread('lab_img.jpg')
image = cv2.imread('C:\\Users\\Administrator\\Pictures\\lab_ia\\progetto_lampioni\\data\\immagine_lab_ia (1).jpg')

# Individua gli illuminanti nell'immagine
illuminanti = individua_illuminanti_immagine(image)

# Disegna i centroidi degli illuminanti sull'immagine originale
for illuminante in illuminanti:
    cv2.circle(image, illuminante, 5, (0, 255, 0), -1)

# Visualizza l'immagine con gli illuminanti individuati
cv2.imshow('Illuminanti individuati', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
