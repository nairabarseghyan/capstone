# import modules 
import pickle
import os
import time 

from data_prep import load_and_preprocess_data, split_data, get_x_y
from features import add_calendar_features, add_sales_proxies, X_y_target_encoder, full_data_target_encoder
from models import ML_model_test, ML_model_ensemble
from config import MODEL_PATH, SEED, seed_everything

os.environ['KMP_DUPLICATE_LIB_OK']='True'
seed_everything(SEED)

start_time = time.time()
#loading data and adding necessary features
initial_data = load_and_preprocess_data(encoding=True)
features_data_calendar = add_calendar_features(initial_data)
features_data_proxies = add_sales_proxies(features_data_calendar)

#spliting data
train_data, val_data, test_data = split_data(features_data_proxies)


# X y split 
train_X_raw, train_y, validate_X_raw, validate_y, test_X_raw, test_y = get_x_y(train_data, val_data, test_data)

# Encoding Categorical variables
train_X, validate_X, test_X, encoder = X_y_target_encoder(train_X_raw, train_y, 
                                                     validate_X_raw, test_X_raw, 
                                                     return_encoder = True)





######################### Modeling ##########################


# testing multiple ML models
test_models = ML_model_test(train_X, train_y, validate_X, validate_y)


# Final ensamble model
ensemble_models = ML_model_ensemble(train_X, train_y, validate_X, validate_y)


final_model = ensemble_models[2]


# Saving Final Model 

filename = 'ensemble_model.sav'

model_path = os.path.join(MODEL_PATH, filename)  # Ensures the path concatenation is correct
with open(model_path, 'wb') as file:
    pickle.dump(final_model, file)



# Saving Encoder
encoder_name = 'ml_target_encoder.pkl'
encoder_path = os.path.join(MODEL_PATH, encoder_name)  # Ensures the path concatenation is correct
with open(encoder_path, 'wb') as file:
    pickle.dump(encoder, file)

print("Machine Learning models training process is completed in --- %s seconds ---" % (time.time() - start_time))