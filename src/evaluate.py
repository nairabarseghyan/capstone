#IMPORTS 
## Libraries
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
import numpy as np
import pandas as pd
from gluonts.evaluation import Evaluator

# Import custom functionalities 
from config import DATA_PATH






def evaluate_model(y_true_train, y_pred_train, y_true_val, y_pred_val, model_name):
    """
    Evaluate a machine learning model's performance with various metrics for both training and validation sets.

    Parameters:
    - y_true_train (array): True values for the training set.
    - y_pred_train (array): Predicted values for the training set.
    - y_true_val (array): True values for the validation set.
    - y_pred_val (array): Predicted values for the validation set.
    - model_name (str): Name of the model being evaluated.

    Outputs:
    - Saves a CSV file with evaluation metrics for each set and prints them.
    """
    
    # Calculate various error metrics for training and validation sets
    mae_train = mean_absolute_error(y_true_train, y_pred_train)
    mae_val = mean_absolute_error(y_true_val, y_pred_val)
    
    mape_train = mean_absolute_percentage_error(y_true_train, y_pred_train)
    mape_val = mean_absolute_percentage_error(y_true_val, y_pred_val)
    
    rmse_train = np.sqrt(mean_squared_error(y_true_train, y_pred_train))
    rmse_val = np.sqrt(mean_squared_error(y_true_val, y_pred_val))
    
    r2_train = r2_score(y_true_train, y_pred_train)
    r2_val = r2_score(y_true_val, y_pred_val)
    
    
    metrics = {
        "model_name": model_name,
        "mae_train": mae_train,
        "mae_val": mae_val,
        "mape_train": mape_train,
        "mape_val": mape_val,
        "rmse_train": rmse_train,
        "rmse_val": rmse_val,
        "r2_train": r2_train,
        "r2_val": r2_val
    }
    
    # Convert dictionary to DataFrame
    metrics_df = pd.DataFrame([metrics])
    
    metrics_df.to_csv(f'{DATA_PATH}results/Models/{model_name}.csv',index = False)
    
    # Print evaluation results    
    print(f"Results of model {model_name}: ")
    
    print("MAE (Mean Absolute Error):")
    print(f"Train Set: {mae_train}")
    print(f"Validation Set: {mae_val}\n")
    
    print("MAPE (Mean Absolute Percentage Error):")
    print(f"Train Set: {mape_train}%")
    print(f"Validation Set: {mape_val}%\n")
    
    print("RMSE (Root Mean Squared Error):")
    print(f"Train Set: {rmse_train}")
    print(f"Validation Set: {rmse_val}\n")
    
    print("R-squared (R2) Score:")
    print(f"Train Set: {r2_train}")
    print(f"Validation Set: {r2_val}\n")
    
    
    
def evaluate_lag_llama_model(tss_val, forecasts_val, test_data, prediction_length, model_name):
    """
    Evaluate the lag-llama model using GluonTS's built-in Evaluator and custom calculations.

    Parameters:
    - tss_val (Iterable): Validation true time series data.
    - forecasts_val (Iterable): Predictions from the lag-llama model.
    - test_data (DataFrame): Original test dataset.
    - prediction_length (int): Length of the forecast horizon.
    - model_name (str): Name of the model being evaluated.

    Outputs:
    - Saves a CSV file with evaluation metrics and prints them.
    """
    
    # Create an evaluator and calculate aggregate metric
    evaluator = Evaluator()

    agg_metrics_val, ts_metrics_val = evaluator(iter(tss_val), iter(forecasts_val))
        
    # Calculate specific metrics
    mae_val = agg_metrics_val["abs_error"] / prediction_length
    mape_val = agg_metrics_val["MAPE"]
    rmse_val = agg_metrics_val["RMSE"]
    r2_val = r2_score(test_data[0]['target'], forecasts_val[0].quantile(0.5))
    

    
    metrics = {
        "model_name": model_name,
        "mae_val": mae_val,
        "mape_val": mape_val,
        "rmse_val": rmse_val,
        "r2_val": r2_val
    }
        
    # Save metrics to a CSV file
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(f'{DATA_PATH}results/Models/{model_name}.csv',index = False)
        
    # Print evaluation results    
    print(f"Results of model {model_name}: ")
    print("MAE (Mean Absolute Error):")   
    print(f"Validation Set: {mae_val}\n")     
     
    print("MAPE (Mean Absolute Percentage Error):")
    print(f"Validation Set: {mape_val}%\n")    
    
    print("RMSE (Root Mean Squared Error):")
    print(f"Validation Set: {rmse_val}\n")   
     
    print("R-squared (R2) Score:")
    print(f"Validation Set: {r2_val}\n")
        
    