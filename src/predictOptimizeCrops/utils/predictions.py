#CER done
import numpy as np

def predict_top_10_crops(model, scaler, new_data):
    """
    Predict the top 10 crops based on the model and scaler provided.
    
    Parameters:
    - model: Trained machine learning model with `predict_proba` method.
    - scaler: Scaler used to normalize or standardize the data.
    - new_data: 2D array of new data to predict (shape: [n_samples, n_features]).
    
    Returns:
    - top_10_crops: List of the top 10 predicted crop names based on probabilities.
    
    Raises:
    - ValueError: If new_data is empty or has incorrect dimensions.
    - AttributeError: If the model or scaler do not have the expected methods.
    """
    # Check if model and scaler have required methods
    if not hasattr(model, 'predict_proba') or not hasattr(scaler, 'transform'):
        raise AttributeError("The model must have a 'predict_proba' method and the scaler must have a 'transform' method.")
    
    # Validate new_data dimensions
    if new_data.ndim != 2 or new_data.shape[1] != scaler.n_features_in_:
        raise ValueError("New data must be a 2D array with the same number of features as the scaler was trained on.")
    
    # Transform new data using the scaler
    new_data_scaled = scaler.transform(new_data)
    
    # Predict probabilities for each class
    probabilities = model.predict_proba(new_data_scaled)[0]
    
    # Get the top 10 crop predictions based on highest probabilities
    top_10_crops = [model.classes_[i] for i in np.argsort(probabilities)[::-1][:10]]
    
    return top_10_crops

def predict_interactive(model, scaler, input_ph, input_temperature, input_rainfall, input_humidity, 
                        input_nitrogen, input_phosphorus, input_potassium, input_o2):
    """
    Predict the top 10 crops based on interactive user inputs.
    
    Parameters:
    - model: Trained machine learning model with `predict_proba` method.
    - scaler: Scaler used to normalize or standardize the data.
    - input_ph: pH level of the soil (float).
    - input_temperature: Temperature in Celsius (float).
    - input_rainfall: Rainfall amount (float).
    - input_humidity: Humidity percentage (float).
    - input_nitrogen: Nitrogen level (float).
    - input_phosphorus: Phosphorus level (float).
    - input_potassium: Potassium level (float).
    - input_o2: Oxygen level (float).
    
    Returns:
    - top_10_predictions: List of the top 10 predicted crop names based on the input data.
    
    Raises:
    - ValueError: If any input value is missing or not of the correct type.
    """
    # Validate input types
    inputs = [input_ph, input_temperature, input_rainfall, input_humidity, input_nitrogen, 
              input_phosphorus, input_potassium, input_o2]
    if any(not isinstance(i, (int, float)) for i in inputs):
        raise ValueError("All inputs must be numerical values.")
    
    # Create a numpy array from the user inputs
    new_data = np.array([[input_ph, input_temperature, input_rainfall, input_humidity, 
                          input_nitrogen, input_phosphorus, input_potassium, input_o2]])
    
    # Predict the top 10 crops based on the new data
    top_10_predictions = predict_top_10_crops(model, scaler, new_data)
    
    return top_10_predictions
