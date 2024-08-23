import pandas as pd

def load_crop_financial_data(file_path, crops):
    df = pd.read_csv(file_path)
    filtered_df = df[df['Crop'].isin(crops)]
    cost_per_m2 = filtered_df['cost_per_area'].tolist()
    weight_area = filtered_df['weight_area'].tolist()
    amount_area = filtered_df['amount_area'].tolist()

    revenue_per_m2 = [w * a for w, a in zip(weight_area, amount_area)]
    
    return cost_per_m2, weight_area, revenue_per_m2
