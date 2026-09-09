import numpy as np
import pandas as pd
import os

BIHAR_DISTRICTS = [
    "Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", "Bhagalpur", "Bhojpur", "Buxar",
    "Darbhanga", "East Champaran (Motihari)", "Gaya", "Gopalganj", "Jamui", "Jehanabad",
    "Kaimur", "Katihar", "Khagaria", "Kishanganj", "Lakhisarai", "Madhepura", "Madhubani",
    "Munger", "Muzaffarpur", "Nalanda", "Nawada", "Patna", "Purnia", "Rohtas", "Saharsa",
    "Samastipur", "Saran (Chhapra)", "Sheikhpura", "Sheohar", "Sitamarhi", "Siwan",
    "Supaul", "Vaishali (Hajipur)", "West Champaran (Bettiah)"
]

def get_bihar_complete_geo_hierarchy():
    hierarchy = {
        "East Champaran (Motihari)": {
            "Motihari Sadar Sub-Div": ["Motihari Sadar", "Turkaulia", "Piprakothi", "Kotwa", "Sugauli", "Banjariya"],
            "Chakia Sub-Div": ["Chakia", "Kalyanpur", "Kesaria", "Madhuban", "Mehsi", "Tetariya"],
            "Raxaul Sub-Div": ["Raxaul", "Adapur", "Ramgarhwa", "Chauradano"],
            "Sikrahna (Dhaka) Sub-Div": ["Dhaka", "Ghorasahan", "Bankatwa", "Chiraiya", "Patahi"],
            "Areraj Sub-Div": ["Areraj", "Paharpur", "Harsidhi", "Sangrampur"]
        },
        "Muzaffarpur": {
            "Muzaffarpur East Sub-Div": ["Musahari", "Kanti", "Motipur", "Gaighat", "Bochahan", "Minapur", "Bandra"],
            "Muzaffarpur West Sub-Div": ["Marwan", "Paroo", "Sahebganj", "Saraiya", "Sakra", "Kurhani", "Aurai", "Katra"]
        },
        "Patna": {
            "Patna Sadar Sub-Div": ["Patna Sadar", "Phulwari Sharif", "Sampatchak"],
            "Danapur Sub-Div": ["Danapur", "Maner", "Dinapur-Naubatpur", "Bihta"],
            "Barh Sub-Div": ["Barh", "Bakhtiarpur", "Mokama", "Pandarak", "Ghoswari", "Athmalgola"],
            "Patna City Sub-Div": ["Patna City", "Fatwah", "Daniyawan"],
            "Masaurhi Sub-Div": ["Masaurhi", "Dhanarua", "Punpun"],
            "Paliganj Sub-Div": ["Paliganj", "Dulhin Bazar", "Bikram"]
        },
        "Gaya": {
            "Gaya Sadar Sub-Div": ["Gaya Town", "Bodh Gaya", "Manpur", "Belaganj", "Wazirganj", "Fatehpur"],
            "Tekari Sub-Div": ["Tekari", "Konch", "Guraru", "Paraiya"],
            "Sherghati Sub-Div": ["Sherghati", "Amas", "Barachatti", "Dobhi", "Gurua", "Bankey Bazar"],
            "Neemchak Bathani Sub-Div": ["Bathani", "Atri", "Mohra", "Khizirsarai"]
        },
        "Darbhanga": {
            "Darbhanga Sadar Sub-Div": ["Darbhanga Sadar", "Keoti", "Singhchwara", "Jale", "Manigachhi", "Bahadurpur"],
            "Benipur Sub-Div": ["Benipur", "Baheri", "Alinagar", "Biraul"],
            "Biraul Sub-Div": ["Biraul Block", "Ghanshyampur", "Kiratpur", "Kusheshwar Asthan", "Kusheshwar Asthan East"]
        },
        "Bhagalpur": {
            "Bhagalpur Sadar Sub-Div": ["Jagdishpur", "Nathnagar", "Sultanganj", "Sabour", "Ghoraiya"],
            "Kahalgaon Sub-Div": ["Kahalgaon", "Pirmapainti", "Sanokhar"],
            "Naugachia Sub-Div": ["Naugachia", "Bihpur", "Gopalpur", "Kharik", "Narayanpur", "Rangra Chowk"]
        }
    }
    for dist in BIHAR_DISTRICTS:
        if dist not in hierarchy:
            hierarchy[dist] = {
                f"{dist} Sadar Sub-Division": [f"{dist} Sadar", f"{dist} East Block", f"{dist} West Block", f"{dist} Central"],
                f"{dist} Rural Sub-Division": [f"{dist} North Block", f"{dist} South Block", f"{dist} Rural Area"]
            }
    return hierarchy

def generate_paimana_2026_dataset(n_records=3500, save_path="data/paimana_processed.csv"):
    np.random.seed(42)
    geo_dict = get_bihar_complete_geo_hierarchy()
    
    work_categories = [
        "National/State Highway 4-Lane Road Work",
        "Railway Overbridge (ROB) & Flyover Construction",
        "Har Ghar Nal Ka Jal Mega Overhead Water Tank & Supply",
        "Railway Double Line & Track Electrification Work",
        "Urban Storm Drainage & Flood Embankment Protection"
    ]
    
    contractors = [
        "L&T Infrastructure Limited", "Dilip Buildcon Ltd.", "Afcons Infrastructure",
        "Bihar Dynamic Infra - Joint Venture", "Tata Projects Ltd.", "NCC Limited",
        "GVR Infra Projects", "Patel Engineering"
    ]

    records = []
    for i in range(1, n_records + 1):
        dist = np.random.choice(BIHAR_DISTRICTS)
        subdiv_list = list(geo_dict[dist].keys())
        subdiv = np.random.choice(subdiv_list)
        block_list = geo_dict[dist][subdiv]
        block = np.random.choice(block_list)
        work_type = np.random.choice(work_categories)
        
        orig_cost = float(np.round(np.random.uniform(150.0, 3800.0), 2))
        orig_dur = int(np.random.randint(18, 60))
        elapsed = int(np.random.randint(4, orig_dur + 8))
        
        planned_pct = float(np.clip((elapsed / orig_dur) * 100.0, 5.0, 100.0))
        phys_pct = float(np.clip(planned_pct * np.random.uniform(0.35, 1.05), 3.0, 98.0))
        
        spend_ratio = np.random.uniform(0.85, 1.45)
        cum_exp = float(np.round(np.clip((orig_cost * (phys_pct / 100.0)) * spend_ratio, 15.0, orig_cost * 1.8), 2))
        
        del_milestones = int(np.random.poisson(lam=2.6))
        revisions = int(np.random.choice([0, 1, 2, 3], p=[0.52, 0.28, 0.15, 0.05]))
        land_risk = float(np.round(np.random.uniform(3.0, 9.5), 1))
        inflation_idx = float(np.round(np.random.uniform(108.0, 138.0), 1))
        
        sched_variance = float(np.round(phys_pct - planned_pct, 1))
        spend_burn = float(np.round(cum_exp / elapsed, 2))
        
        cost_overrun = float(np.clip(
            (revisions * 12.5) + (del_milestones * 3.3) + (land_risk * 2.2) +
            ((inflation_idx - 100.0) * 0.42) - (sched_variance * 0.38) +
            np.random.normal(0, 3.2), 0.0, 150.0
        ))
        
        time_overrun = float(np.clip(
            (del_milestones * 3.2) + (revisions * 7.0) + (land_risk * 1.7) -
            (sched_variance * 0.30) + np.random.normal(0, 2.2), 0.0, 60.0
        ))

        records.append({
            'project_id': f"BHR_{dist[:3].upper()}_2026_{i:04d}",
            'project_name': f"{work_type} - {block} ({dist})",
            'state': 'Bihar',
            'district': dist,
            'subdivision': subdiv,
            'block': block,
            'project_type': work_type,
            'contractor': np.random.choice(contractors),
            'je_incharge': f"Er. {np.random.choice(['A. K. Mishra', 'R. K. Singh', 'Vikash Kumar', 'S. N. Pandey', 'Manoj Tiwary'])} (Site Camp, {block})",
            'ae_incharge': f"Er. {np.random.choice(['Rajeshwar Prasad', 'M. P. Sinha', 'K. K. Jha', 'Sunil Verma'])} (Div Office, {dist})",
            'original_cost_cr': orig_cost,
            'original_duration_months': orig_dur,
            'elapsed_months': elapsed,
            'cumulative_expenditure_cr': cum_exp,
            'physical_progress_pct': np.round(phys_pct, 1),
            'delayed_milestones_count': del_milestones,
            'revisions_count': revisions,
            'land_acquisition_risk_score': land_risk,
            'material_inflation_idx': inflation_idx,
            'planned_progress_pct': np.round(planned_pct, 1),
            'schedule_variance_pct': sched_variance,
            'spend_burn_rate': spend_burn,
            'cost_overrun_pct': np.round(cost_overrun, 1),
            'time_overrun_months': np.round(time_overrun, 1)
        })

    df = pd.DataFrame(records)
    os.makedirs("data", exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"Data Generation Completed: {len(df)} 2026 Bihar projects saved to '{save_path}'")
    return df

if __name__ == "__main__":
    generate_paimana_2026_dataset()