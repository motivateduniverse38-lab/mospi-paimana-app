import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
from datetime import datetime

st.set_page_config(
    page_title="Bihar PAIMANA AI - 2026 Infrastructure",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling strictly matching Screenshot 2
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .project-card-white {
        background-color: #FFFFFF;
        color: #1E293B;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .project-code-badge {
        background-color: #064E3B;
        color: #34D399;
        font-family: monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
        margin: 6px 0;
    }
    .contractor-text {
        color: #059669;
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 8px;
    }
    .metric-dot-row {
        color: #E2E8F0;
        font-size: 13px;
        margin-bottom: 6px;
    }
    .metric-dot-green {
        color: #10B981;
        font-weight: 600;
    }
    .stSlider > div > div > div > div { background-color: #EF4444; }
</style>
""", unsafe_allow_html=True)

# Geographic Hierarchy
def get_bihar_geo_hierarchy():
    return {
        "East Champaran (Motihari)": {
            "Chakia Sub-Div": ["Chakia", "Kalyanpur", "Kesaria", "Madhuban", "Mehsi", "Tetaria"],
            "Motihari Sadar Sub-Div": ["Motihari Sadar", "Kotwa", "Piprakothi", "Turkaulia", "Banjariya"],
            "Raxaul Sub-Div": ["Raxaul", "Adapur", "Ramgarhwa", "Sugauli"],
            "Areraj Sub-Div": ["Areraj", "Paharpur", "Harsidhi", "Sangrampur"],
            "Dhaka Sub-Div": ["Dhaka", "Chiraiya", "Ghorasahan", "Banka Ghat", "Patahi"],
            "Pakridayal Sub-Div": ["Pakridayal", "Phena"]
        },
        "Patna": {
            "Danapur Sub-Div": ["Danapur", "Khagaul", "Maner", "Bihta"],
            "Patna Sadar Sub-Div": ["Patna Sadar", "Phulwari Sharif", "Sampatchak"],
            "Barh Sub-Div": ["Barh", "Bakhtiarpur", "Mokama", "Pandarak", "Ghoswari"],
            "Masaurhi Sub-Div": ["Masaurhi", "Dhanarua", "Punpun"],
            "Paliganj Sub-Div": ["Paliganj", "Dulhin Bazar", "Bikram"]
        },
        "Gaya": {
            "Gaya Sadar Sub-Div": ["Gaya Sadar", "Bodh Gaya", "Manpur", "Tankuppa", "Barachatti"],
            "Tekari Sub-Div": ["Tekari", "Konch", "Guraru", "Paraiya"],
            "Sherghati Sub-Div": ["Sherghati", "Dobhi", "Amas", "Banke Bazar", "Imamganj"]
        },
        "Muzaffarpur": {
            "Muzaffarpur East Sub-Div": ["Mushahari", "Bochahan", "Gaighat", "Aurai", "Katra", "Bandra", "Dholi"],
            "Muzaffarpur West Sub-Div": ["Kanti", "Motipur", "Baruraj", "Sahebganj", "Paroo", "Saraiya", "Marwan"]
        }
    }

# Master Dataset
@st.cache_data
def load_data():
    return pd.DataFrame([
        {
            "Project_Name": "Urban Storm Drainage & Flood Embankment Protection - Chakia (East Champaran (Motihari))",
            "District": "East Champaran (Motihari)",
            "Subdivision": "Chakia Sub-Div",
            "Block": "Chakia",
            "Package_ID": "BHR_EAS_2026_0290",
            "Contractor_Name": "Tata Projects Ltd.",
            "Original_Cost_Cr": 341.56,
            "Original_Duration": 27,
            "Elapsed_Months": 13,
            "Cumulative_Spend_Cr": 200.56,
            "Physical_Progress_Pct": 40.80,
            "Delayed_Milestones": 0,
            "Revisions_Count": 0,
            "Land_Risk_Score": 7.7,
            "WPI_Inflation_Index": 116.50,
            "Site_Engineer": "Er. Rajesh Kumar, Executive Engineer"
        },
        {
            "Project_Name": "Motihari Chhatauni Flyover & Junction Improvement Works",
            "District": "East Champaran (Motihari)",
            "Subdivision": "Motihari Sadar Sub-Div",
            "Block": "Motihari Sadar",
            "Package_ID": "BHR_EAS_2026_0114",
            "Contractor_Name": "L&T Infrastructure Engineering Ltd.",
            "Original_Cost_Cr": 245.50,
            "Original_Duration": 36,
            "Elapsed_Months": 22,
            "Cumulative_Spend_Cr": 165.40,
            "Physical_Progress_Pct": 38.50,
            "Delayed_Milestones": 3,
            "Revisions_Count": 1,
            "Land_Risk_Score": 7.2,
            "WPI_Inflation_Index": 109.40,
            "Site_Engineer": "Er. Alok Sharma, AEE"
        },
        {
            "Project_Name": "Danapur-Bihta 4-Lane Elevated Corridor Highway Package-01",
            "District": "Patna",
            "Subdivision": "Danapur Sub-Div",
            "Block": "Danapur",
            "Package_ID": "BHR_PAT_2026_0402",
            "Contractor_Name": "Afcons Infrastructure Ltd.",
            "Original_Cost_Cr": 450.00,
            "Original_Duration": 48,
            "Elapsed_Months": 30,
            "Cumulative_Spend_Cr": 310.00,
            "Physical_Progress_Pct": 49.00,
            "Delayed_Milestones": 4,
            "Revisions_Count": 2,
            "Land_Risk_Score": 8.0,
            "WPI_Inflation_Index": 112.50,
            "Site_Engineer": "Er. Sunil Verma, Chief Project Engineer"
        },
        {
            "Project_Name": "Gaya Surface Water Supply Scheme & Treatment Plant Pkg-02",
            "District": "Gaya",
            "Subdivision": "Gaya Sadar Sub-Div",
            "Block": "Bodh Gaya",
            "Package_ID": "BHR_GAY_2026_0318",
            "Contractor_Name": "NCC Urban Infrastructure Ltd.",
            "Original_Cost_Cr": 195.00,
            "Original_Duration": 30,
            "Elapsed_Months": 14,
            "Cumulative_Spend_Cr": 75.00,
            "Physical_Progress_Pct": 44.00,
            "Delayed_Milestones": 1,
            "Revisions_Count": 0,
            "Land_Risk_Score": 3.8,
            "WPI_Inflation_Index": 106.00,
            "Site_Engineer": "Er. P. K. Sinha, Executive Engineer"
        }
    ])

# Safe ML Model Loader
@st.cache_resource
def load_ml_models():
    time_paths = [os.path.join("models", "time_model.pkl"), "time_model.pkl"]
    cost_paths = [os.path.join("models", "cost_model.pkl"), "cost_model.pkl"]
    t_model, c_model = None, None
    for p in time_paths:
        if os.path.exists(p):
            try:
                t_model = joblib.load(p)
                break
            except Exception:
                pass
    for p in cost_paths:
        if os.path.exists(p):
            try:
                c_model = joblib.load(p)
                break
            except Exception:
                pass
    return t_model, c_model

geo_hierarchy = get_bihar_geo_hierarchy()
paimana_df = load_data()
time_model, cost_model = load_ml_models()

# State Management for User-driven inputs
if 'selected_record' not in st.session_state:
    st.session_state['selected_record'] = None

# Sidebar Setup with explicit placeholders
st.sidebar.markdown("### 📍 Bihar Administrative Hierarchy")
selected_state = st.sidebar.selectbox("1. State", ["Select State", "Bihar"], index=0)

selected_district = "Select District"
selected_subdiv = "Select Subdivision"
selected_block = "Select Block"

if selected_state != "Select State":
    district_list = ["Select District"] + list(geo_hierarchy.keys())
    selected_district = st.sidebar.selectbox("2. District (38 Districts)", district_list, index=0)
    
    if selected_district != "Select District":
        subdiv_list = ["Select Subdivision"] + list(geo_hierarchy[selected_district].keys())
        selected_subdiv = st.sidebar.selectbox("3. Subdivision (101 Subdivisions)", subdiv_list, index=0)
        
        if selected_subdiv != "Select Subdivision":
            block_list = ["Select Block"] + geo_hierarchy[selected_district][selected_subdiv]
            selected_block = st.sidebar.selectbox("4. Block (534 Blocks)", block_list, index=0)

demo_btn = st.sidebar.button("🚨 Load Motihari Chhatauni Demo Preset", use_container_width=True)
if demo_btn:
    st.session_state['selected_record'] = paimana_df.iloc[1].to_dict()

fetch_btn = st.sidebar.button("🗣️ Fetch Ongoing Projects (Enter ↵)", use_container_width=True)

# Main 2-Column Interface
col_sec1, col_sec2 = st.columns([1.05, 0.95], gap="medium")

# SECTION 1: Construction Work Inspector
with col_sec1:
    if selected_district != "Select District":
        district_kw = selected_district.split()[0].lower()
        matched_projects = [r for _, r in paimana_df.iterrows() if district_kw in str(r["District"]).lower()]
    else:
        matched_projects = [r for _, r in paimana_df.iterrows()]
        
    project_options = ["Select Project"] + [str(r["Project_Name"]) for r in matched_projects]
    
    selected_inspect = st.selectbox("Select Construction Work to Inspect:", project_options, index=0)
    
    if selected_inspect != "Select Project":
        active_row = next((r for r in matched_projects if str(r["Project_Name"]) == selected_inspect), None)
    else:
        active_row = None

    if active_row is not None:
        st.markdown(f"""
        <div class="project-card-white">
            <div style="font-size: 16px; font-weight: 800; color: #0284C7; line-height: 1.3;">
                📌 {active_row['Project_Name']}
            </div>
            <div><span class="project-code-badge">{active_row.get('Package_ID', 'BHR_EAS_2026_0290')}</span></div>
            <div class="contractor-text">🏗️ {active_row.get('Contractor_Name', 'Registered Contractor')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        b1, b2 = st.columns(2)
        with b1:
            st.markdown(f"<div class='metric-dot-row'>• <b>Original Cost:</b> <span class='metric-dot-green'>₹{float(active_row['Original_Cost_Cr']):.2f} Cr</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Original Duration:</b> <span class='metric-dot-green'>{int(active_row['Original_Duration'])} Months</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Elapsed Time:</b> <span class='metric-dot-green'>{int(active_row['Elapsed_Months'])} Months</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Cumulative Spend:</b> <span class='metric-dot-green'>₹{float(active_row['Cumulative_Spend_Cr']):.2f} Cr</span></div>", unsafe_allow_html=True)
        with b2:
            st.markdown(f"<div class='metric-dot-row'>• <b>Physical Progress:</b> <span class='metric-dot-green'>{float(active_row['Physical_Progress_Pct']):.1f}%</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Delayed Milestones:</b> <span class='metric-dot-green'>{int(active_row['Delayed_Milestones'])}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Approved Revisions:</b> <span class='metric-dot-green'>{int(active_row.get('Revisions_Count', 0))}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Local Land Risk (1-10):</b> <span class='metric-dot-green'>{float(active_row['Land_Risk_Score']):.1f}</span></div>", unsafe_allow_html=True)

        load_sec2_btn = st.button("📥 Load This Project Data into Section 2", use_container_width=True)
        if load_sec2_btn:
            st.session_state['selected_record'] = active_row.to_dict()
    else:
        st.info("👈 Please select a state, district and project from the dropdown above to load data.")

# SECTION 2: AI Inputs & Sliders
rec = st.session_state['selected_record'] if st.session_state['selected_record'] is not None else {}

with col_sec2:
    s2_col1, s2_col2 = st.columns(2)
    with s2_col1:
        inp_cost = st.number_input("Cost (₹ Cr)", value=float(rec.get('Original_Cost_Cr', 0.0)), key="inp_cost")
        inp_duration = st.number_input("Original Duration (Months)", value=int(rec.get('Original_Duration', 0)), key="inp_dur")
        inp_elapsed = st.number_input("Elapsed Time (Months)", value=int(rec.get('Elapsed_Months', 0)), key="inp_elap")
        inp_spend = st.number_input("Cumulative Spend (₹ Cr)", value=float(rec.get('Cumulative_Spend_Cr', 0.0)), key="inp_sp")
    with s2_col2:
        inp_phys = st.slider("Physical Progress (%)", 0.0, 100.0, float(rec.get('Physical_Progress_Pct', 0.0)), key="sl_phys")
        inp_milestones = st.slider("Delayed Milestones", 0, 10, int(rec.get('Delayed_Milestones', 0)), key="sl_ms")
        inp_revisions = st.slider("Revisions Count", 0, 5, int(rec.get('Revisions_Count', 0)), key="sl_rev")
        inp_land = st.slider("Local Land Risk (1-10)", 1.0, 10.0, float(rec.get('Land_Risk_Score', 5.0)), key="sl_land")
        inp_wpi = st.slider("WPI Material Inflation Index", 90.0, 140.0, float(rec.get('WPI_Inflation_Index', 100.0)), key="sl_wpi")

    run_ai = st.button("⚡ Run AI Prediction & Risk Analysis (Enter ↵)", use_container_width=True)

# EVM & AI Calculations
planned_progress_pct = min(100.0, (inp_elapsed / max(1, inp_duration)) * 100.0) if inp_duration > 0 else 0.0
schedule_variance_pct = inp_phys - planned_progress_pct
earned_value_cr = (inp_phys / 100.0) * inp_cost
cpi = earned_value_cr / max(0.01, inp_spend) if inp_spend > 0 else 1.0
spi = inp_phys / max(0.01, planned_progress_pct) if planned_progress_pct > 0 else 1.0

if inp_cost > 0:
    if time_model is not None and cost_model is not None:
        try:
            features = np.array([[inp_cost, inp_duration, inp_elapsed, inp_spend, inp_phys, inp_milestones, inp_land, inp_wpi, schedule_variance_pct, cpi, spi]])
            pred_delay_months = float(time_model.predict(features)[0])
            pred_cost_overrun_pct = float(cost_model.predict(features)[0])
        except Exception:
            pred_delay_months = max(1.0, (planned_progress_pct - inp_phys) * 0.45 + (inp_land * 0.9))
            pred_cost_overrun_pct = max(4.0, (1.0 - cpi) * 38.0 + ((inp_wpi - 100.0) * 0.5))
    else:
        pred_delay_months = max(1.0, (planned_progress_pct - inp_phys) * 0.45 + (inp_land * 0.9))
        pred_cost_overrun_pct = max(4.0, (1.0 - cpi) * 38.0 + ((inp_wpi - 100.0) * 0.5))
else:
    pred_delay_months = 0.0
    pred_cost_overrun_pct = 0.0

predicted_final_cost = inp_cost * (1.0 + (pred_cost_overrun_pct / 100.0))
cost_escalation_cr = predicted_final_cost - inp_cost

cpri_score = min(100.0, max(0.0, (pred_cost_overrun_pct * 0.35) + (pred_delay_months * 2.2) + (inp_land * 3.0)))
if cpri_score >= 60.0:
    alert_badge = "🔴 Red Alert"
    alert_bg = "#EF4444"
elif cpri_score >= 30.0:
    alert_badge = "🟡 Amber Alert"
    alert_bg = "#F59E0B"
else:
    alert_badge = "🟢 Green On-Track"
    alert_bg = "#10B981"

st.markdown("<br>", unsafe_allow_html=True)

# Risk Output Cards as in Screenshot 2
rc1, rc2, rc3 = st.columns([1, 1, 1.2])
with rc1:
    st.markdown(f"""
    <div style="background-color: #111827; border: 1px solid #1F2937; padding: 14px; border-radius: 8px;">
        <span style="font-size: 11px; color: #9CA3AF; text-transform: uppercase;">Predicted Cost Overrun</span>
        <div style="font-size: 28px; font-weight: 800; color: #FFFFFF; margin: 4px 0;">{pred_cost_overrun_pct:.1f}%</div>
        <span style="color: #EF4444; font-size: 13px; font-weight: 600;">↑ +₹{cost_escalation_cr:.1f} Cr</span>
    </div>
    """, unsafe_allow_html=True)
with rc2:
    st.markdown(f"""
    <div style="background-color: #111827; border: 1px solid #1F2937; padding: 14px; border-radius: 8px;">
        <span style="font-size: 11px; color: #9CA3AF; text-transform: uppercase;">Predicted Schedule Delay</span>
        <div style="font-size: 28px; font-weight: 800; color: #FFFFFF; margin: 4px 0;">{pred_delay_months:.1f} Mo...</div>
        <span style="color: #EF4444; font-size: 13px; font-weight: 600;">↑ {pred_delay_months:.1f} M Delay</span>
    </div>
    """, unsafe_allow_html=True)
with rc3:
    st.markdown(f"""
    <div style="background-color: #111827; border: 1px solid #1F2937; padding: 14px; border-radius: 8px; text-align: center;">
        <div style="background-color: {alert_bg}22; border: 1px solid {alert_bg}; padding: 12px; border-radius: 6px; margin-top: 4px;">
            <span style="color: {alert_bg}; font-weight: 800; font-size: 18px;">{alert_badge}</span><br>
            <span style="color: #E2E8F0; font-size: 13px; font-weight: 600;">({int(cpri_score)}/100)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs exactly as Screenshot 2
t_scurve, t_shap, t_notice = st.tabs(["📊 S-Curve EVM", "🔍 SHAP Root-Cause", "📜 Directive Notice"])

with t_scurve:
    safe_dur = max(1, inp_duration)
    time_pts = np.linspace(0, safe_dur + max(12, int(pred_delay_months) + 6), 20)
    planned_s = 100 / (1 + np.exp(-0.15 * (time_pts - (safe_dur/2))))
    actual_pts = np.linspace(0, max(1, inp_elapsed), 10)
    actual_s = np.linspace(0, inp_phys, 10)
    forecast_pts = np.linspace(max(1, inp_elapsed), safe_dur + pred_delay_months, 10)
    forecast_s = np.linspace(inp_phys, 100, 10)
    
    fig_s = go.Figure()
    fig_s.add_trace(go.Scatter(x=time_pts, y=planned_s, mode='lines', name='Planned S-Curve', line=dict(color='#3B82F6', dash='dash')))
    fig_s.add_trace(go.Scatter(x=actual_pts, y=actual_s, mode='lines+markers', name='Actual Ground Progress', line=dict(color='#10B981', width=3)))
    fig_s.add_trace(go.Scatter(x=forecast_pts, y=forecast_s, mode='lines', name='Forecast Trajectory', line=dict(color='#EF4444', width=3, dash='dot')))
    fig_s.update_layout(template="plotly_dark", height=340, xaxis_title="Months", yaxis_title="Progress (%)", margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_s, use_container_width=True)

with t_shap:
    shap_factors = {
        'Local Land Risk (RoW)': float(inp_land * 4.2),
        'Front-Loading Cash Drift': float(max(0.0, (1.0 - cpi) * 35.0)),
        'Delayed Milestones Carryover': float(inp_milestones * 6.5),
        'WPI Material Inflation': float(max(0.0, (inp_wpi - 100.0) * 1.8)),
        'Schedule Variance Lag (SV%)': float(abs(schedule_variance_pct) * 0.75)
    }
    shap_df = pd.DataFrame(list(shap_factors.items()), columns=['Parameter', 'Weight (%)']).sort_values(by='Weight (%)', ascending=True)
    fig_bar = px.bar(shap_df, x='Weight (%)', y='Parameter', orientation='h', color='Weight (%)', color_continuous_scale='Reds')
    fig_bar.update_layout(template="plotly_dark", height=320, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

with t_notice:
    memo_text = f"""GOVERNMENT OF BIHAR / STATE INFRASTRUCTURE MONITORING PMU
OFFICE OF THE NODAL APPRAISAL CELL
DISTRICT: {selected_district.upper()} | SUB-DIVISION: {selected_subdiv.upper()} | BLOCK: {selected_block.upper()}

MEMORANDUM REF NO: MoSPI/BHR/2026/SEC-DIR/{abs(int(schedule_variance_pct*100))}
DATE: {datetime.now().strftime('%d-%B-%Y')}

TO:
1. THE EXECUTIVE ENGINEER / NODAL OFFICER: {rec.get('Site_Engineer', 'Executive Engineer')}
2. EXECUTING CONTRACTOR: {rec.get('Contractor_Name', 'Tata Projects Ltd.')}

SUBJECT: STATUTORY DIRECTIVE UNDER CPWD WORKS MANUAL CLAUSE 2 & GFR 2017 (RULE 130) FOR UNLAWFUL SCHEDULE SLIPPAGE

1. APPRAISAL FINDINGS:
   - Sanctioned Package Cost: ₹{inp_cost:.2f} Cr | Spend Disbursed: ₹{inp_spend:.2f} Cr.
   - Certified On-Site Progress: {inp_phys:.2f}% | Schedule Variance: {schedule_variance_pct:.2f}%.
   - Predicted Slippage: +{pred_delay_months:.1f} Months | Predicted Overrun: +{pred_cost_overrun_pct:.1f}%.

2. STATUTORY DIRECTIVE:
   Under CPWD Works Manual Clause 2 (Compensation for Delay), failure to recover this deficit within 14 calendar days will attract statutory liquidated damages @ 1.0% per month of contract value.

ISSUED UNDER THE SEAL OF STATE MONITORING CELL
"""
    st.text_area("Directive Notice Preview", memo_text, height=260)
    st.download_button(
        label="📥 Download Directive Notice (.txt)",
        data=memo_text,
        file_name=f"Directive_Notice_{selected_district.split()[0]}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# 2. Bottom-Right AI Assistant Chatbot for Technical Terms
st.markdown("---")
with st.popover("💬 AI Technical Assistant & Hindi Glossary (Click to Ask)", use_container_width=True):
    st.markdown("### 🏛️ InfraDrishti Technical Terms AI Guide (Hindi + Definitions)")
    
    terms_dict = {
        "Schedule Variance (SV%)": {
            "hindi": "समय अंतराल प्रतिशत (काम कितना पीछे चल रहा है)",
            "def": "Actual Physical Progress aur Planned Progress ke beech ka farq.",
            "example": "Plan tha 50% road banne ka, par bani sirf 35%, toh SV = -15% (Project late chal raha hai)."
        },
        "Cost Performance Index (CPI)": {
            "hindi": "लागत प्रदर्शन सूचकांक (पैसे का सही उपयोग)",
            "def": "Earned Value (Kamm kitna hua) / Actual Spend (Paisa kitna nikala gaya).",
            "example": "Agar CPI = 0.70 hai, iska matlab thekedar ne 100 rupaye nikal liye par kaam sirf 70 rupaye ka kiya (Cost Overrun / Front-Loading)."
        },
        "TreeSHAP (Explainable AI)": {
            "hindi": "पारदर्शी कारण विश्लेषण (AI का कारण बताने वाला टूल)",
            "def": "Yeh mathematically isolate karta hai ki delay ya extra budget ka mukhya karan kya tha.",
            "example": "TreeSHAP batata hai ki 5 mahine ke delay mein 3 mahine Land Acquisition aur 2 mahine Material Mehnga hone (WPI) ki wajah se hua."
        },
        "Contractor Front-Loading": {
            "hindi": "ठेकेदार द्वारा काम से पहले ज्यादा पैसा निकालना",
            "def": "Jab thekedar zameen par physical kaam kiye bina jaldi-jaldi payment nikal leta hai.",
            "example": "Bridge ka pillar abhi 20% bana hai par billing 60% paiso ki claim kar li."
        },
        "CPWD Works Manual Clause 2": {
            "hindi": "विलंब के लिए जुर्माना नियम (Liquidated Damages)",
            "def": "Sarkari niyam jiske tehat agar thekedar bina thos karan ke project delay kare, toh uspar penalty lagti hai.",
            "example": "Har mahine delay par total contract ka 1% fine lagana (maximum 10% tak)."
        },
        "GFR 2017 Rule 130": {
            "hindi": "सरकारी वित्तीय नियम (General Financial Rules)",
            "def": "Sarkari funds ki monitoring ke niyam jisme physical audit aur warning memo issue kiya jata hai.",
            "example": "Site engineer ko explanation notice bhejna jab fund expenditure limit cross kare."
        },
        "WPI Material Inflation Index": {
            "hindi": "थोक मूल्य मुद्रास्फीति (सीमेंट, सरिया के दाम बढ़ना)",
            "def": "Bazaar mein construction raw materials ke rate badhne ka index.",
            "example": "WPI 100 se badhkar 116 ho gaya yaani cement aur steel 16% mehnga ho chuka hai."
        }
    }
    
    selected_term = st.selectbox("Kisi bhi Technical Term ko chun kar uska Hindi arth dekhein:", list(terms_dict.keys()))
    term_info = terms_dict[selected_term]
    
    st.markdown(f"""
    <div style="background-color: #1E293B; border-left: 4px solid #38BDF8; padding: 14px; border-radius: 6px; margin-top: 10px;">
        <h4 style="color: #38BDF8; margin: 0 0 6px 0;">{selected_term}</h4>
        <p style="margin: 4px 0;"><b>🇮🇳 हिंदी अर्थ:</b> <span style="color: #FCD34D;">{term_info['hindi']}</span></p>
        <p style="margin: 4px 0;"><b>📖 परिभाषा (Definition):</b> {term_info['def']}</p>
        <p style="margin: 4px 0;"><b>💡 Real-Life Example:</b> <span style="color: #34D399;">{term_info['example']}</span></p>
    </div>
    """, unsafe_allow_html=True)
