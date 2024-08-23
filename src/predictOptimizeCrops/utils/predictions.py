import numpy as np

def predict_top_10_crops(model, scaler, new_data):
    new_data_scaled = scaler.transform(new_data)
    probabilities = model.predict_proba(new_data_scaled)[0]
    top_10_crops = [model.classes_[i] for i in np.argsort(probabilities)[::-1][:10]]
    return top_10_crops

def predict_interactive(model, scaler, input_ph, input_temperature, input_rainfall, input_humidity, 
                        input_nitrogen, input_phosphorus, input_potassium, input_o2):
    new_data = np.array([[input_ph, input_temperature, input_rainfall, input_humidity, 
                          input_nitrogen, input_phosphorus, input_potassium, input_o2]])
    top_10_predictions = predict_top_10_crops(model, scaler, new_data)
    return top_10_predictions
