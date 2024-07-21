import tensorflow as tf
import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler


# Load the model and scalers once at startup
loaded_model = tf.keras.models.load_model('./Models/AgrisistanceModel.h5')
X = joblib.load('./Data/X_data.pkl')
encoder = joblib.load('./Data/encoder.pkl')
scaler = StandardScaler().fit(X)

def predict_crops(model, scaler, encoder, input_data, top_percentage=0.2):
    # Scale the input data
    input_data_scaled = scaler.transform([input_data])
    
    # Make predictions
    predictions = model.predict(input_data_scaled)
    top_n = int(predictions.shape[1] * top_percentage)
    top_indices = np.argsort(predictions[0])[-top_n:][::-1]
    
    predicted_crops = encoder.inverse_transform(np.eye(predictions.shape[1])[top_indices])
    
    return predicted_crops

def get_predictions(input_params):
    print(f"Input parameters: {input_params}")
    input_data = np.array(input_params)
    scaler = StandardScaler().fit(X)
    predicted_crops = predict_crops(loaded_model, scaler, encoder, input_data)
    return predicted_crops

