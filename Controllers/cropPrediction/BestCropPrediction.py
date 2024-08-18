import numpy as np
import joblib
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the model and scaler
def load_model(model_path, scaler_path):
    logging.info("Loading model and scaler...")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

# Predict top 20 crops based on similarity
def predict_top_20_crops(model, scaler, new_data):
    logging.info("Predicting top 20 crops...")
    new_data_scaled = scaler.transform(new_data)
    probabilities = model.predict_proba(new_data_scaled)[0]
    top_20_crops = sorted(
        [(model.classes_[i], probabilities[i]) for i in range(len(probabilities))],
        key=lambda x: x[1], reverse=True
    )[:20]
    return top_20_crops

# Interactive prediction function
def predict_interactive(model, scaler, InputData):
    logging.info("Preparing data for prediction...")
    
    new_data = np.array([[float(value) for value in InputData]])
    top_20_predictions = predict_top_20_crops(model, scaler, new_data)
    
    logging.info("Top 20 crop predictions:")
    
    # Create a list to store crop names
    crop_names = [crop for crop, _ in top_20_predictions]
    
    return crop_names
                    
def BestCropPredictionMain(InputData):
    # Load the model and scaler
    model_file = './Models/knn_crop_model.joblib'  # Path to your saved model
    scaler_file = './Models/knn_crop_scaler.joblib'  # Path to your saved scaler
    knn_model, scaler = load_model(model_file, scaler_file)

    # Run the interactive prediction
    return predict_interactive(knn_model, scaler, InputData)
