import cv2
from sklearn.metrics import precision_score, recall_score, f1_score

def calculate_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

    iou = intersection / float(area1 + area2 - intersection)
    return iou

# Bounding box ottenuti da cv2.boundingRect()
bounding_boxes_cv2 = [(0.0, 0.0, 293.0, 3.0), (0.0, 197.0, 250.0, 3.0), (0.0, 242.0, 216.0, 3.0), (0.0, 235.0, 201.0, 5.0), (0.0, 221.0, 164.0, 9.0), (0.0, 163.0, 48.0, 31.0)]

# Bounding box dal testo delle etichettature di Roboflow
bounding_boxes_roboflow = [(0.0, 0.31953125, 0.19765625, 0.03828125), (0.0, 0.40546875, 0.53515625, 0.0359375), (0.0, 0.42421875, 0.6453125, 0.021875), (0.0, 0.43515625, 0.69140625, 0.01796875), (0.0, 0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0, 0.0)]

# Rimuovi elementi aggiuntivi dalla lista bounding_boxes_roboflow
bounding_boxes_roboflow = bounding_boxes_roboflow[:len(bounding_boxes_cv2)]

# Converti i bounding box nel formato (xmin, ymin, xmax, ymax)
bounding_boxes_cv2 = [(box[0], box[1], box[0] + box[2], box[1] + box[3]) for box in bounding_boxes_cv2]

# Crea le liste di target e predizioni
y_true = [0] * len(bounding_boxes_roboflow)
y_pred = [0] * len(bounding_boxes_cv2)

# Calcola la corrispondenza tra i bounding box
for i, cv2_box in enumerate(bounding_boxes_cv2):
    cv2_xmin, cv2_ymin, cv2_xmax, cv2_ymax = cv2_box

    for j, roboflow_box in enumerate(bounding_boxes_roboflow):
        roboflow_xmin, roboflow_ymin, roboflow_xmax, roboflow_ymax = roboflow_box

        iou = calculate_iou(cv2_box, (roboflow_xmin, roboflow_ymin, roboflow_xmax, roboflow_ymax))

        if iou > 0.5:
            y_pred[i] = 1
            y_true[j] = 1
            break

# Calcola le metriche di valutazione
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

# Stampa i risultati
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)
