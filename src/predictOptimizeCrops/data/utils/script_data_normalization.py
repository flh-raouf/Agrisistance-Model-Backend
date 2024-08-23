import pandas as pd
import numpy as np

input_file = 'primary.csv'  
df = pd.read_csv(input_file)

output_data = []

for index, row in df.iterrows():
    crop = row['Crop']
    minO2 = row['minO2']
    maxO2 = row['maxO2']
    
    for _ in range(1000):
        ph = int(np.random.randint(row['MinPH'], row['MaxPH'] + 1))
        temp = int(np.random.randint(row['MinTemp'], row['MaxTemp'] + 1))
        rain = int(np.random.randint(row['MinRain'], row['MaxRain'] + 1))
        humidity = int(np.random.randint(row['MinHumidity'], row['MaxHumidity'] + 1))
        n = int(np.random.randint(row['MinN'], row['MaxN'] + 1))
        p = int(np.random.randint(row['MinP'], row['MaxP'] + 1))
        k = int(np.random.randint(row['MinK'], row['MaxK'] + 1))
        o2 = int(np.random.randint(minO2, maxO2 + 1))
        
        output_data.append([crop, ph, temp, rain, humidity, n, p, k, o2])

output_df = pd.DataFrame(output_data, columns=['Crop', 'pH', 'Temp', 'Rain', 'Humidity', 'Nitrogen', 'Phosphorus', 'Potassium', 'Oxygen'])
output_file = 'trainable_data.csv'
output_df.to_csv(output_file, index=False)

print(f'Output has been saved to {output_file}')
