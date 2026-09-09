import streamlit as st
import numpy as np
import pandas as pd
import pickle
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from src.data_prep import get_bihar_complete_geo_hierarchy
from src.explainability import compute_project_shap_drivers

# Compact Page Configuration
st.set_page_config(
    page_title="MoSPI PAIMANA | 2026 Infrastructure Monitor",
    layout="wide",
    page_icon="🏛️"
)

# Ultra-Compact Viewport CSS (Zero unnecessary scroll)
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    .gov-header { 
        font-size: 20px; 
        font-weight: 700; 
        color: #1a365d; 
        border-bottom: 2px solid #c53030;
        padding-bottom: 2px;
        margin-bottom: 1px;
    }
    .gov-sub { 
        font-size: 11px; 
        color: #4a5568; 
        margin-bottom: 8px; 
    }
    .stat-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #2b6cb0;
        padding: 6px 10px;
        border-radius: 4px;
        font-size: 12px;
        margin-bottom: 6px;
    }
    .sec-title {
        font-size: 14px;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 4px;
    }
    .empty-state {
        background: #f8fafc;
        border: 1px dashed #cbd5e0;
        padding: 15px;
        text-align: center;
        color: #718096;
        border-radius: 4px;
        font-size: 12px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 18px !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 11px !important;
    }
    .stSlider, .stNumberInput {
        margin-bottom: -15px !important;
    }
    </style>
""", unsafe_allow_html=True)

current_time_str = datetime.now().strftime("%d-%b-%Y | %H:%M:%S IST")
st.markdown('<div class="gov-header">PROJECT APPRAISAL & INFRASTRUCTURE MONITORING ENGINE (PAIMANA)</div>', unsafe_allow_html=True)
st.markdown(f'<div class="gov-sub">MoSPI Infrastructure Monitoring Division | State PMU (Bihar) | Live System Timestamp: <b>{current_time_str}</b></div>', unsafe_allow_html=True)

@st.cache_resource
def load_system_resources():
    with open("models/cost_model.pkl", "rb") as f:
        c_model = pickle.load(f)
    with open("models/time_model.pkl", "rb") as f:
        t_model = pickle.load(f)
    df = pd.read_csv("data/paimana_processed.csv")
    return c_model, t_model, df

try:
    cost_model, time_model, full_df = load_system_resources()
except Exception:
    st.error("⚠️ Model artifacts missing. Terminal me execute karein: `python -m src.data_prep` & `python -m src.train`")
    st.stop()

geo_hierarchy = get_bihar_complete_geo_hierarchy()

# --- SIDEBAR: STRICT PLACEHOLDERS ---
st.sidebar.markdown("### 🏛️ Administrative Jurisdiction")
state_options = ["Select State", "Bihar"]
sel_state = st.sidebar.selectbox("1. State", state_options, index=1)

dist_list = ["Select District"] + sorted(list(geo_hierarchy.keys()))
sel_dist = st.sidebar.selectbox("2. District (38 Districts)", dist_list, index=10 if "East Champaran (Motihari)" in dist_list else 0)

subdiv_list = ["Select Subdivision"]
if sel_dist != "Select District":
    subdiv_list += list(geo_hierarchy[sel_dist].keys())
sel_subdiv = st.sidebar.selectbox("3. Subdivision (101 Sub-Div)", subdiv_list, index=1 if len(subdiv_list) > 1 else 0)

block_list = ["Select Block"]
if sel_subdiv != "Select Subdivision":
    block_list += geo_hierarchy[sel_dist][sel_subdiv]
sel_block = st.sidebar.selectbox("4. Block (534 Blocks)", block_list, index=1 if len(block_list) > 1 else 0)

st.sidebar.divider()
btn_fetch = st.sidebar.button("Fetch Registered Works Record")

if btn_fetch:
    if sel_dist == "Select District" or sel_subdiv == "Select Subdivision" or sel_block == "Select Block":
        st.sidebar.warning("⚠️ Select complete administrative hierarchy.")
    else:
        st.session_state['data_retrieved'] = True

# Screen Layout: 2 Compact Columns
col_left, col_right = st.columns([1, 1.15])

# ==========================================
# SECTION 1: COMPACT WORKS REGISTRY
# ==========================================
with col_left:
    st.markdown('<div class="sec-title">📁 Section 1: Official Infrastructure Registry</div>', unsafe_allow_html=True)

    if not st.session_state.get('data_retrieved', False):
        st.markdown("""
        <div class="empty-state">
            <b>No Active Jurisdiction Queried</b><br>
            Select district and block from sidebar, then click 'Fetch Registered Works Record'.
        </div>
        """, unsafe_allow_html=True)
    else:
        matched = full_df[(full_df['district'] == sel_dist) & (full_df['block'] == sel_block)]
        if matched.empty:
            matched = full_df[full_df['district'] == sel_dist].head(5)

        proj_names = list(matched['project_name'].values)
        sel_proj = st.selectbox("Select Project to Inspect:", proj_names, label_visibility="collapsed")
        row = matched[matched['project_name'] == sel_proj].iloc[0]

        st.markdown(f"""
        <div class="stat-card">
            <b>Code:</b> <code>{row['project_id']}</code> | <b>Type:</b> {row['project_type']}<br>
            <b>Contractor:</b> <span style="color:#2b6cb0; font-weight:600;">{row['contractor']}</span><br>
            <b>JE:</b> {row['je_incharge']} | <b>AE:</b> {row['ae_incharge']}
        </div>
        """, unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        with m1:
            st.caption(f"• **Cost:** `₹{row['original_cost_cr']:.2f} Cr` | **Duration:** `{row['original_duration_months']}M`")
            st.caption(f"• **Elapsed:** `{row['elapsed_months']}M` | **Spent:** `₹{row['cumulative_expenditure_cr']:.2f} Cr`")
        with m2:
            st.caption(f"• **Physical Progress:** `{row['physical_progress_pct']}%`")
            st.caption(f"• **Delayed Milestones:** `{row['delayed_milestones_count']}` | **Land Risk:** `{row['land_acquisition_risk_score']}`")

        if st.button("➡️ Load into Section 2 Engine", use_container_width=True):
            st.session_state['active_proj_name'] = row['project_name']
            st.session_state['val_cost'] = float(row['original_cost_cr'])
            st.session_state['val_dur'] = int(row['original_duration_months'])
            st.session_state['val_elapsed'] = int(row['elapsed_months'])
            st.session_state['val_exp'] = float(row['cumulative_expenditure_cr'])
            st.session_state['val_phys'] = float(row['physical_progress_pct'])
            st.session_state['val_del'] = int(row['delayed_milestones_count'])
            st.session_state['val_rev'] = int(row['revisions_count'])
            st.session_state['val_land'] = float(row['land_acquisition_risk_score'])
            st.session_state['val_inf'] = float(row['material_inflation_idx'])
            st.session_state['val_contractor'] = row['contractor']
            st.session_state['val_je'] = row['je_incharge']
            st.session_state['val_ae'] = row['ae_incharge']
            st.session_state['appraisal_evaluated'] = False
            st.rerun()

# ==========================================
# SECTION 2: NO-SCROLL RISK APPRAISAL ENGINE
# ==========================================
with col_right:
    st.markdown('<div class="sec-title">⚡ Section 2: Predictive Risk Appraisal Engine</div>', unsafe_allow_html=True)

    with st.form("compact_appraisal_form"):
        proj_heading = st.session_state.get('active_proj_name', 'Active Evaluation Scope')
        st.caption(f"**Target:** `{proj_heading}`")
        
        # Grid layout for inputs to minimize height
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            inp_cost = st.number_input("Cost (₹ Cr)", min_value=0.0, value=st.session_state.get('val_cost', 0.0), format="%.1f")
            inp_phys = st.number_input("Progress (%)", 0.0, 100.0, st.session_state.get('val_phys', 0.0), step=1.0)
        with r2:
            inp_dur = st.number_input("Target (M)", min_value=0, value=st.session_state.get('val_dur', 0), step=1)
            inp_del = st.number_input("Delayed M/S", 0, 15, st.session_state.get('val_del', 0), step=1)
        with r3:
            inp_elapsed = st.number_input("Elapsed (M)", min_value=0, value=st.session_state.get('val_elapsed', 0), step=1)
            inp_land = st.number_input("Land Risk (1-10)", 1.0, 10.0, st.session_state.get('val_land', 1.0), step=0.5)
        with r4:
            inp_exp = st.number_input("Spend (₹ Cr)", min_value=0.0, value=st.session_state.get('val_exp', 0.0), format="%.1f")
            inp_inf = st.number_input("WPI Index", 90.0, 150.0, st.session_state.get('val_inf', 100.0), step=1.0)

        inp_rev = st.session_state.get('val_rev', 1)
        submit_appraisal = st.form_submit_button("⚡ Run AI Evaluation (Single Viewport)", use_container_width=True)

    if submit_appraisal:
        if inp_cost == 0.0 or inp_dur == 0:
            st.error("⚠️ Cost/Duration cannot be zero.")
        else:
            st.session_state['appraisal_evaluated'] = True

    if st.session_state.get('appraisal_evaluated', False):
        safe_dur = max(inp_dur, 1)
        safe_elapsed = max(inp_elapsed, 1)
        
        planned_val_pct = min((safe_elapsed / safe_dur) * 100.0, 100.0)
        sched_variance = inp_phys - planned_val_pct
        spend_burn = inp_exp / safe_elapsed
        earned_val = (inp_cost * (inp_phys / 100.0))
        actual_cost = max(inp_exp, 0.01)
        cpi = earned_val / actual_cost
        spi = inp_phys / max(planned_val_pct, 0.01)

        feat_arr = np.array([[inp_cost, inp_dur, inp_elapsed, inp_exp, inp_phys, inp_del, inp_rev, sched_variance, spend_burn, inp_land, inp_inf]])
        pred_cost_pct = float(cost_model.predict(feat_arr)[0])
        pred_time_mon = float(time_model.predict(feat_arr)[0])
        
        effective_del = max(1, int(pred_time_mon // 4)) if (pred_time_mon > 6.0 and inp_del == 0) else inp_del
        revised_cost = inp_cost * (1.0 + pred_cost_pct / 100.0)
        risk_composite = min(100.0, max(0.0, (pred_cost_pct * 0.45) + (pred_time_mon * 1.6)))

        # 3 Metrics side-by-side directly below form
        k1, k2, k3 = st.columns(3)
        k1.metric("Predicted Cost Overrun", f"{pred_cost_pct:.1f}%", f"+₹{revised_cost - inp_cost:.1f} Cr", delta_color="inverse")
        k2.metric("Schedule Delay", f"{pred_time_mon:.1f} M", f"{pred_time_mon:.1f} Months", delta_color="inverse")
        if risk_composite < 30:
            k3.success(f"🟢 Low ({risk_composite:.0f}/100)")
        elif risk_composite < 60:
            k3.warning(f"🟡 Amber ({risk_composite:.0f}/100)")
        else:
            k3.error(f"🔴 Red Alert ({risk_composite:.0f}/100)")

        # Ultra-Compact Tabs (Height = 160px so everything fits on 1 screen)
        t1, t2, t3 = st.tabs(["📊 EVM Audit", "🔍 SHAP Root-Cause", "📜 Memorandum"])
        
        with t1:
            fig_s = go.Figure()
            fig_s.add_trace(go.Bar(name='Planned', x=['Progress'], y=[planned_val_pct], marker_color='#3182ce'))
            fig_s.add_trace(go.Bar(name='Actual', x=['Progress'], y=[inp_phys], marker_color='#38a169'))
            fig_s.update_layout(barmode='group', height=140, margin=dict(l=5, r=5, t=10, b=5))
            st.plotly_chart(fig_s, use_container_width=True)
            st.caption(f"• **SV:** `{sched_variance:.1f}%` | **CPI:** `{cpi:.2f}` | **SPI:** `{spi:.2f}` | **Burn:** `₹{spend_burn:.2f} Cr/M`")

        with t2:
            input_dict = {
                'original_cost_cr': inp_cost, 'original_duration_months': inp_dur, 'elapsed_months': inp_elapsed,
                'cumulative_expenditure_cr': inp_exp, 'physical_progress_pct': inp_phys,
                'delayed_milestones_count': effective_del, 'revisions_count': inp_rev,
                'schedule_variance_pct': sched_variance, 'spend_burn_rate': spend_burn,
                'land_acquisition_risk_score': inp_land, 'material_inflation_idx': inp_inf
            }
            shap_res = compute_project_shap_drivers(input_dict)
            top_df = pd.DataFrame({'Driver': shap_res.index[:4], 'Score': shap_res.values[:4]}).sort_values(by='Score')
            fig_shap = px.bar(top_df, x='Score', y='Driver', orientation='h', color='Score', color_continuous_scale='Reds', height=140)
            fig_shap.update_layout(margin=dict(l=5, r=5, t=10, b=5))
            st.plotly_chart(fig_shap, use_container_width=True)

        with t3:
            c_name = st.session_state.get('val_contractor', 'Lead Contractor')
            c_je = st.session_state.get('val_je', f'JE ({sel_block})')
            c_ae = st.session_state.get('val_ae', f'AE ({sel_dist})')
            memo_no = f"MoSPI/BHR/{sel_dist[:3].upper()}/2026/ENC-{np.random.randint(100, 999)}"
            st.markdown(f"""
            <div style="background:#fff; border:1px solid #111; padding:8px; border-radius:3px; font-size:11.5px; color:#111 !important; line-height:1.3;">
                <b>MEMO NO:</b> <code>{memo_no}</code> | <b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}<br>
                <b>Agency:</b> {c_name} | <b>Officers:</b> {c_ae}, {c_je}<br>
                <b>Directive:</b> Under CPWD Manual Clause 2 & GFR 130, rectify schedule slippage ({abs(sched_variance):.1f}%) within 10 days. CPI at {cpi:.2f} requires physical-spend audit.
            </div>
            """, unsafe_allow_html=True)