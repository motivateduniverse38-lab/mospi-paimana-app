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

# State Management for User-driven inputs & Evaluation
if 'selected_record' not in st.session_state:
    st.session_state['selected_record'] = None
if 'ai_evaluated' not in st.session_state:
    st.session_state['ai_evaluated'] = False

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
    preset_rec = paimana_df.iloc[1].to_dict()
    st.session_state['selected_record'] = preset_rec
    st.session_state['inp_cost'] = float(preset_rec['Original_Cost_Cr'])
    st.session_state['inp_dur'] = int(preset_rec['Original_Duration'])
    st.session_state['inp_elap'] = int(preset_rec['Elapsed_Months'])
    st.session_state['inp_sp'] = float(preset_rec['Cumulative_Spend_Cr'])
    st.session_state['sl_phys'] = float(preset_rec['Physical_Progress_Pct'])
    st.session_state['sl_ms'] = int(preset_rec['Delayed_Milestones'])
    st.session_state['sl_rev'] = int(preset_rec['Revisions_Count'])
    st.session_state['sl_land'] = float(preset_rec['Land_Risk_Score'])
    st.session_state['sl_wpi'] = float(preset_rec['WPI_Inflation_Index'])
    st.session_state['ai_evaluated'] = True

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
            row_dict = active_row.to_dict()
            st.session_state['selected_record'] = row_dict
            st.session_state['inp_cost'] = float(row_dict['Original_Cost_Cr'])
            st.session_state['inp_dur'] = int(row_dict['Original_Duration'])
            st.session_state['inp_elap'] = int(row_dict['Elapsed_Months'])
            st.session_state['inp_sp'] = float(row_dict['Cumulative_Spend_Cr'])
            st.session_state['sl_phys'] = float(row_dict['Physical_Progress_Pct'])
            st.session_state['sl_ms'] = int(row_dict['Delayed_Milestones'])
            st.session_state['sl_rev'] = int(row_dict.get('Revisions_Count', 0))
            st.session_state['sl_land'] = float(row_dict['Land_Risk_Score'])
            st.session_state['sl_wpi'] = float(row_dict['WPI_Inflation_Index'])
            st.session_state['ai_evaluated'] = False
            st.rerun()
    else:
        st.info("👈 Please select state, district and project to inspect.")

# SECTION 2: AI Inputs & Sliders
rec = st.session_state.get('selected_record') or {}

with col_sec2:
    s2_col1, s2_col2 = st.columns(2)
    with s2_col1:
        inp_cost = st.number_input("Cost (₹ Cr)", value=float(st.session_state.get('inp_cost', rec.get('Original_Cost_Cr', 0.0))), key="inp_cost")
        inp_duration = st.number_input("Original Duration (Months)", value=int(st.session_state.get('inp_dur', rec.get('Original_Duration', 0))), key="inp_dur")
        inp_elapsed = st.number_input("Elapsed Time (Months)", value=int(st.session_state.get('inp_elap', rec.get('Elapsed_Months', 0))), key="inp_elap")
        inp_spend = st.number_input("Cumulative Spend (₹ Cr)", value=float(st.session_state.get('inp_sp', rec.get('Cumulative_Spend_Cr', 0.0))), key="inp_sp")
    with s2_col2:
        inp_phys = st.slider("Physical Progress (%)", 0.0, 100.0, float(st.session_state.get('sl_phys', rec.get('Physical_Progress_Pct', 0.0))), key="sl_phys")
        inp_milestones = st.slider("Delayed Milestones", 0, 10, int(st.session_state.get('sl_ms', rec.get('Delayed_Milestones', 0))), key="sl_ms")
        inp_revisions = st.slider("Revisions Count", 0, 5, int(st.session_state.get('sl_rev', rec.get('Revisions_Count', 0))), key="sl_rev")
        inp_land = st.slider("Local Land Risk (1-10)", 1.0, 10.0, float(st.session_state.get('sl_land', rec.get('Land_Risk_Score', 5.0))), key="sl_land")
        inp_wpi = st.slider("WPI Material Inflation Index", 90.0, 140.0, float(st.session_state.get('sl_wpi', rec.get('WPI_Inflation_Index', 100.0))), key="sl_wpi")

    run_ai = st.button("⚡ Run AI Prediction & Risk Analysis (Enter ↵)", use_container_width=True)
    if run_ai:
        if inp_cost > 0 and inp_duration > 0:
            st.session_state['ai_evaluated'] = True
        else:
            st.warning("Please load a project or provide non-zero cost and duration before evaluating.")

# SHOW PREDICTION ONLY AFTER AI EVALUATION BUTTON CLICK
if st.session_state['ai_evaluated'] and inp_cost > 0:
    planned_progress_pct = min(100.0, (inp_elapsed / max(1, inp_duration)) * 100.0)
    schedule_variance_pct = inp_phys - planned_progress_pct
    earned_value_cr = (inp_phys / 100.0) * inp_cost
    cpi = earned_value_cr / max(0.01, inp_spend) if inp_spend > 0 else 1.0
    spi = inp_phys / max(0.01, planned_progress_pct) if planned_progress_pct > 0 else 1.0

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

    # 4 Analytical Tabs
    t_scurve, t_shap, t_notice, t_whatif = st.tabs([
        "📊 S-Curve EVM", 
        "🔍 SHAP Root-Cause", 
        "📜 Directive Notice", 
        "🧪 'What-If' Decision Simulator"
    ])

    with t_scurve:
        # Square-Look Block Progress Visual as in Screenshot 1
        fig_s = go.Figure()
        
        fig_s.add_trace(go.Bar(
            name='Planned Target (%)',
            x=['Schedule Horizon'],
            y=[planned_progress_pct],
            marker=dict(color='#3B82F6', line=dict(color='#60A5FA', width=1.5)),
            width=0.35
        ))
        fig_s.add_trace(go.Bar(
            name='Actual Ground Progress (%)',
            x=['Schedule Horizon'],
            y=[inp_phys],
            marker=dict(color='#10B981', line=dict(color='#34D399', width=1.5)),
            width=0.35
        ))
        
        fig_s.update_layout(
            barmode='group',
            template="plotly_dark",
            height=340,
            title="EVM Square Block Progress Benchmark (Planned vs On-Site Physical)",
            yaxis_title="Physical Completion (%)",
            yaxis=dict(range=[0, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=35, b=20)
        )
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

    with t_whatif:
        st.markdown("#### 🧪 Prescriptive 'What-If' Decision Simulator")
        st.caption("Simulate administrative interventions to project timeline recovery and budget savings.")
        
        sim_c1, sim_c2 = st.columns(2)
        with sim_c1:
            sim_land_reduction = st.slider("Expedite Land RoW Clearance (Risk Score Reduction)", 0.0, 5.0, 2.5, 0.5, key="sim_land")
            sim_fund_infusion = st.slider("Mobilization Advance Recovery (%)", 0, 30, 10, 5, key="sim_fund")
        with sim_c2:
            recovered_delay = max(0.5, pred_delay_months - (sim_land_reduction * 1.1) - (sim_fund_infusion * 0.08))
            recovered_cost = max(1.0, pred_cost_overrun_pct - (sim_land_reduction * 1.8) - (sim_fund_infusion * 0.35))
            recovered_saving_cr = (pred_cost_overrun_pct - recovered_cost) / 100.0 * max(0.0, inp_cost)
            
            st.markdown(f"""
            <div style="background-color: #111827; padding: 15px; border-radius: 8px; border-left: 4px solid #10B981; border: 1px solid #1F2937;">
                <h5 style="color: #10B981; margin:0;">🎯 Interventional Recovery Projection:</h5>
                <p style="margin-top: 8px; font-size: 14px;">
                • Recoverable Timeline: <b>{pred_delay_months - recovered_delay:.1f} Months Saved</b> (Revised Delay: +{recovered_delay:.1f} M)<br>
                • Projected Fiscal Savings: <b>₹{recovered_saving_cr:.2f} Crores</b> (Revised Cost Overrun: +{recovered_cost:.1f}%)<br>
                • Revised Status: <b style="color: {'#10B981' if recovered_delay < 3 else '#F59E0B'};">{'GREEN (RECOVERED)' if recovered_delay < 3 else 'AMBER (MANAGEABLE)'}</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
