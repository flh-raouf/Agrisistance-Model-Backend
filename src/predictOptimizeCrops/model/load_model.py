import joblib
import logging

def load_model(model_file):
    logging.info("Loading the machine learning model...")
    model = joblib.load(model_file)
    return model

def load_scaler(scaler_file):
    logging.info("Loading the scaler...")
    return joblib.load(scaler_file)
