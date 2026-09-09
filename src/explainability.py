import shap
import pickle
import pandas as pd
import numpy as np

def compute_project_shap_drivers(input_data_dict):
    """
    Computes top drivers causing cost overrun for a specific project.
    """
    with open("models/cost_model.pkl", "rb") as f:
        model = pickle.load(f)

    feature_cols = [
        'original_cost_cr', 'original_duration_months', 'elapsed_months',
        'cumulative_expenditure_cr', 'physical_progress_pct',
        'delayed_milestones_count', 'revisions_count', 'schedule_variance_pct',
        'spend_burn_rate', 'land_acquisition_risk_score', 'material_inflation_idx'
    ]

    input_df = pd.DataFrame([input_data_dict])[feature_cols]
    
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(input_df)

    shap_series = pd.Series(shap_values[0], index=feature_cols).sort_values(ascending=False)
    return shap_series