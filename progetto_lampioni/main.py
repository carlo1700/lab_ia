import cv2
import roboflow
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score


# Funzione per l'individuazione degli illuminanti
def individua_illuminanti_immagine(image):
    # Converte l'immagine in scala di grigi
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)


    # Applica una soglia per estrarre i punti di luce
    _, threshold = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    cv2.imshow('threshold', threshold)

    # Applica un filtro per rimuovere il rumore di fondo
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    #immagine binaria
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    cv2.imshow('opening', opening)

    # Trova le componenti connesse nell'immagine binaria
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    illuminanti = []

    # Filtra le regioni connesse per mantenere solo gli illuminanti desiderati
    for contour in contours:
        # Calcola l'area del contorno
        area = cv2.contourArea(contour)

        # Filtra i falsi positivi in base all'area
        if 10 < area < 500:
            # Calcola il centroide del contorno
            moments = cv2.moments(contour)
            # Aggiungi il centroide agli illuminanti individuati
            illuminanti.append((
                moments['m10'] // moments['m00'],
                moments['m01'] // moments['m00']
            ))

    return illuminanti

# Carica l'immagine
image = cv2.imread('roboflow\\test\\images\\immagine_lab_ia-1-_jpg.rf.bbe7082e00bc3ec42ff243f08fd0349b.jpg')

# Individua gli illuminanti nell'immagine
illuminanti = individua_illuminanti_immagine(image)

# Disegna i centroidi degli illuminanti sull'immagine originale
for illuminante in illuminanti:
    x, y = map(int, illuminante)  # Converti le coordinate in valori interi
    cv2.circle(image, (x, y), 5, (0, 255, 0), -1)


# Visualizza l'immagine con gli illuminanti individuati
cv2.imshow('Illuminanti individuati', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Carica l'immagine etichettata da Roboflow
etichette_file = 'roboflow\\test\\labels\\immagine_lab_ia-1-_jpg.rf.bbe7082e00bc3ec42ff243f08fd0349b.txt'

# Leggi le etichette dal file


with open(etichette_file, 'r') as file:
    etichette = [tuple(map(float, line.strip().split())) for line in file]

# Stampa la lunghezza delle etichette e delle predizioni



# Individua gli illuminanti nell'immagine
illuminanti = individua_illuminanti_immagine(image)

# ...

# Inizializzazione della soglia di distanza
soglia_distanza = 10.0  # Imposta una soglia di distanza iniziale arbitraria

# Prepara le predizioni e le etichette corrette per il calcolo delle metriche
predizioni = np.zeros(len(illuminanti), dtype=bool)
for i, (x_predetto, y_predetto) in enumerate(illuminanti):
    # Effettua il confronto con le etichette corrette
    for etichetta in etichette:
        if np.sqrt((x_predetto - etichetta[0]) ** 2 + (y_predetto - etichetta[1]) ** 2) <= soglia_distanza:
            predizioni[i] = True
            break

print(etichette)
print("le etichette sono: ", len(etichette))
print(predizioni)
print("le predizioni sono: ", len(predizioni))

# ...


# Calcola le metriche di precisione, richiamo e F1-score
if len(etichette) != len(predizioni):
    print("Errore: il numero di etichette e predizioni non corrisponde.")
else:
    # Calcola la precisione
    precision = precision_score(etichette, predizioni)
    print("Precisione:", precision)

    # Calcola la recall
    recall = recall_score(etichette, predizioni)
    print("Recall:", recall)

    # Calcola l'F1-score
    f1 = f1_score(etichette, predizioni)
    print("F1-score:", f1)
