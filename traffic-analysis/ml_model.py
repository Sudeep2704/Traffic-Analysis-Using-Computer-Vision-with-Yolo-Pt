from sklearn.ensemble import IsolationForest
import numpy as np

# Train simple anomaly model
model = IsolationForest(contamination=0.05)

def train_model(feature_data):
    model.fit(feature_data)

def predict_anomaly(feature):
    prediction = model.predict([feature])
    return prediction[0] == -1