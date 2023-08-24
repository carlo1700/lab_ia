from sklearn.metrics import precision_score, recall_score, f1_score

# True labels of the test set
y_true = [1, 1, 1, 1, 0]

# Predicted labels of the test set
y_pred = [1, 1, 1, 1, 1]

# Calculate precision score
precision = precision_score(y_true, y_pred, average='micro')

# Calculate recall score
recall = recall_score(y_true, y_pred, average='micro')

# Calculate F1 score
f1 = f1_score(y_true, y_pred, average='micro')

print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)
