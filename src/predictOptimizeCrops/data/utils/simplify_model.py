import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load and preprocess the data
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    X = df[['pH', 'Temp', 'Rain', 'Humidity', 'Nitrogen', 'Phosphorus', 'Potassium', 'Oxygen']].values
    y = df['Crop'].values
    return X, y

# Split data
def split_data(X, y):
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
def scale_features(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled

# Load the original model
model = joblib.load('crop_model.joblib')

# Simplify the model by reducing the number of trees or the depth
simplified_model = RandomForestClassifier(
    n_estimators=50,  # Reduce the number of trees
    max_depth=10,     # Limit the depth of each tree
    random_state=42
)

# Load and preprocess the data
data_file = 'all_trainable_data.csv'
X, y = load_and_preprocess_data(data_file)
X_train, X_test, y_train, y_test = split_data(X, y)
X_train_scaled, X_test_scaled = scale_features(X_train, X_test)

# Fit the simplified model to the training data
simplified_model.fit(X_train_scaled, y_train)

# Save the simplified model
joblib.dump(simplified_model, 'crop_model_simplified.joblib')
