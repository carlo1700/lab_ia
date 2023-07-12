import cv2
import numpy as np


# Carica l'immagine
img = cv2.imread("C:\\Users\\Administrator\\Pictures\\lab_ia\\progetto_lampioni\\data\\immagine_lab_ia (1).jpg")
if img is None:
    print("Immagine non caricata")
    exit()

# Ottieni le dimensioni dell'immagine
imgWidth = img.shape[1]
imgHeight = img.shape[0]

# Imposta le dimensioni desiderate per la visualizzazione
displayWidth = 800
displayHeight = 600

# Calcola i fattori di ridimensionamento per adattare l'immagine alla finestra di visualizzazione
widthRatio = displayWidth / imgWidth
heightRatio = displayHeight / imgHeight
scaleFactor = min(widthRatio, heightRatio)

# Ridimensiona l'immagine mantenendo l'aspetto ratio
img = cv2.resize(img, None, fx=scaleFactor, fy=scaleFactor)

# Converti l'immagine in scala di grigi
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
pippo = np.copy(imgGray)
#crea un keypoint detector
detector = cv2.SimpleBlobDetector_create()
#trova i keypoint
keypoints = detector.detect(pippo)
#disegna i keypoint sull'immagine
pippo = cv2.drawKeypoints(pippo, keypoints, pippo)

cv2.imshow("Immagine in Scala di Grigi", pippo)

# Crea un'istanza dell'oggetto SIFT
sift = cv2.SIFT_create()

# Trova i punti chiave e i descrittori dell'immagine
keypoints, descriptors = sift.detectAndCompute(imgGray, None)

# Disegna i punti chiave sull'immagine originale
imgKeypoints = np.copy(img)
cv2.drawKeypoints(img, keypoints, imgKeypoints)

# Visualizza l'immagine con i punti chiave evidenziati
cv2.imshow("Individuazione Luci", imgKeypoints)
cv2.waitKey(0)

# Trova i lampioni
lampioni = [kp for kp in keypoints if kp.size > 10]

# Disegna i lampioni sull'immagine originale
imgLampioni = np.copy(img)
cv2.drawKeypoints(img, lampioni, imgLampioni)

# Visualizza l'immagine con i lampioni evidenziati
cv2.imshow("Individuazione Lampioni", imgLampioni)
cv2.waitKey(0)
