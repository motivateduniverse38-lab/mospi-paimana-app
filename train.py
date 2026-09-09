import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import Ridge
import lightgbm as lgb

def train_models():
    data_path = "data/paimana_processed.csv"
    if not os.path.exists(data_path):
        from src.data_prep import generate_paimana_2026_dataset
        df = generate_paimana_2026_dataset()
    else:
        df = pd.read_csv(data_path)

    features = [
        'original_cost_cr', 'original_duration_months', 'elapsed_months',
        'cumulative_expenditure_cr', 'physical_progress_pct',
        'delayed_milestones_count', 'revisions_count', 'schedule_variance_pct',
        'spend_burn_rate', 'land_acquisition_risk_score', 'material_inflation_idx'
    ]

    X = df[features]
    y_cost = df['cost_overrun_pct']
    y_time = df['time_overrun_months']

    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_cost, test_size=0.2, random_state=42)
    X_train_t, X_test_t, y_train_t, y_test_t = train_test_split(X, y_time, test_size=0.2, random_state=42)

    # Cost Overrun Model
    model_cost = lgb.LGBMRegressor(n_estimators=250, learning_rate=0.03, max_depth=6, random_state=42)
    model_cost.fit(X_train_c, y_train_c)

    # Time Overrun Model
    model_time = lgb.LGBMRegressor(n_estimators=250, learning_rate=0.03, max_depth=6, random_state=42)
    model_time.fit(X_train_t, y_train_t)

    os.makedirs("models", exist_ok=True)
    with open("models/cost_model.pkl", "wb") as f:
        pickle.dump(model_cost, f)
    with open("models/time_model.pkl", "wb") as f:
        pickle.dump(model_time, f)

    print("Model Training Successful. Artifacts saved in 'models/'.")

if __name__ == "__main__":
    train_models()