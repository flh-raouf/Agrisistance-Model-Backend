import logging
from .model.load_model import load_model, load_scaler
from .utils.load_helpers import load_crop_financial_data
from .utils.predictions import predict_interactive
from .utils.display_results import display_optimal_allocation
from .optimization_algorithm.genetic_algorithm import run_genetic_algorithm

# Genetic Algorithm parameters (optimized)
population_size = 100
num_generations = 400
mutation_rate = 0.1
crossover_rate = 0.8

# Load the model and scaler (unchanged)
model_file = './src/predictOptimizeCrops/model/crop_model_simplified.joblib'
scaler_file = './src/predictOptimizeCrops/model/crop_scaler.joblib'
model = load_model(model_file)
scaler = load_scaler(scaler_file)

# Load crop financial data (unchanged)
crop_finance_file = './src/predictOptimizeCrops/data/crop_finance.csv'

# Logging configuration (unchanged)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def predict_optimize_crops_main(InputData):
    # (unchanged)
    (input_ph, input_temperature, input_rainfall, input_humidity, 
        input_nitrogen, input_phosphorus, input_potassium, input_o2, 
        total_budget, total_area) = InputData
    
    total_budget = int(total_budget)
    total_area = int(total_area)

    crops = predict_interactive(model, scaler, input_ph, input_temperature, input_rainfall, 
                                input_humidity, input_nitrogen, input_phosphorus, input_potassium, input_o2)
        
    cost_per_m2, weight_area, revenue_per_m2 = load_crop_financial_data(crop_finance_file, crops)

    best_solution = run_genetic_algorithm(crops, cost_per_m2, revenue_per_m2, total_area, total_budget, 
                                          population_size, num_generations, mutation_rate, crossover_rate)
    
    OptimizationData = display_optimal_allocation(crops, best_solution, cost_per_m2, weight_area, revenue_per_m2, total_area, total_budget)

    return OptimizationData
