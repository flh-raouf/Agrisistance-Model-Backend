#CER done
import pandas as pd

def load_crop_financial_data(file_path, crops):
    """
    Load crop financial data from a CSV file and compute relevant metrics.
    
    Parameters:
    - file_path: Path to the CSV file containing crop data (string).
    - crops: List of crop names to filter the data (list of strings).
    
    Returns:
    - cost_per_m2: List of cost per square meter for each crop.
    - weight_area: List of weight return per square meter for each crop.
    - revenue_per_m2: List of calculated revenue per square meter for each crop.
    
    Raises:
    - FileNotFoundError: If the specified CSV file does not exist.
    - KeyError: If the required columns are missing in the CSV file.
    - ValueError: If the 'Crop' column contains values not present in the `crops` list.
    """
    
    # Load data from CSV file
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    
    # Check if required columns are present
    required_columns = ['Crop', 'cost_per_area', 'weight_area', 'amount_area']
    if not all(col in df.columns for col in required_columns):
        raise KeyError(f"The CSV file must contain the following columns: {', '.join(required_columns)}")
    
    # Filter the dataframe to include only the specified crops
    filtered_df = df[df['Crop'].isin(crops)]
    
    # Check if any crops were found
    if filtered_df.empty:
        raise ValueError("None of the specified crops were found in the data.")
    
    # Extract relevant columns and compute revenue per square meter
    cost_per_m2 = filtered_df['cost_per_area'].tolist()
    weight_area = filtered_df['weight_area'].tolist()
    amount_area = filtered_df['amount_area'].tolist()

    # Calculate revenue per square meter
    revenue_per_m2 = [w * a for w, a in zip(weight_area, amount_area)]
    
    return cost_per_m2, weight_area, revenue_per_m2
