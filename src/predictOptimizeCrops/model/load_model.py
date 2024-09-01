import joblib
import logging

def load_model(model_file):
    # Log the loading process
    logging.info("Loading the machine learning model...")
    
    # Load and return the model from the file
    model = joblib.load(model_file)
    return model

def load_scaler(scaler_file):
    # Log the loading process
    logging.info("Loading the scaler...")
    
    # Load and return the scaler from the file
    return joblib.load(scaler_file)
