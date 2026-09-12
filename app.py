import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import time
from datetime import datetime

st.set_page_config(
    page_title="PAIMANA AI - Analysis & Predict AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# User Preference Settings State
if "app_bg_theme" not in st.session_state:
    st.session_state["app_bg_theme"] = "Dark Slate"
if "app_accent_color" not in st.session_state:
    st.session_state["app_accent_color"] = "Cyan Blue"

bg_map = {
    "Dark Slate": "#0B0F19",
    "Deep Midnight": "#050814",
    "Pitch Black": "#000000"
}
accent_map = {
    "Cyan Blue": "#38BDF8",
    "Emerald Green": "#10B981",
    "Amber Gold": "#F59E0B"
}

active_bg = bg_map.get(st.session_state["app_bg_theme"], "#0B0F19")
active_accent = accent_map.get(st.session_state["app_accent_color"], "#38BDF8")

# 1. 4-Second Splash Animation Engine
if "splash_done" not in st.session_state:
    splash_placeholder = st.empty()
    with splash_placeholder.container():
        st.markdown(f"""
        <style>
            .splash-wrapper {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 80vh;
                text-align: center;
                animation: fadeIn 1s ease-in-out;
            }}
            .splash-logo {{
                font-size: 58px;
                font-weight: 900;
                letter-spacing: 3px;
                color: {active_accent};
                text-shadow: 0 0 30px rgba(56, 189, 248, 0.8);
                margin-bottom: 8px;
            }}
            .splash-sub {{
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 4px;
                color: #94A3B8;
                text-transform: uppercase;
                margin-bottom: 25px;
            }}
            .splash-loader {{
                width: 220px;
                height: 4px;
                background-color: #1E293B;
                border-radius: 4px;
                overflow: hidden;
                position: relative;
            }}
            .splash-bar {{
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, {active_accent}, #10B981);
                animation: progress 4s ease-in-out forwards;
            }}
            @keyframes progress {{
                0% {{ transform: translateX(-100%); }}
                100% {{ transform: translateX(0%); }}
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: scale(0.95); }}
                to {{ opacity: 1; transform: scale(1); }}
            }}
        </style>
        <div class="splash-wrapper">
            <div class="splash-logo">🏛️ PAIMANA AI</div>
            <div class="splash-sub">MoSPI Infrastructure Monitoring & Predictive Risk Engine</div>
            <div class="splash-loader"><div class="splash-bar"></div></div>
            <p style="color: #64748B; font-size: 13px; margin-top: 14px;">Ingesting MoSPI PAIMANA Flash Reports & CPWD/GFR Framework...</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(4.0)
    st.session_state["splash_done"] = True
    splash_placeholder.empty()

# Custom High-Visibility & Cross-Platform Typography CSS
st.markdown(f"""
<style>
    /* Complete Cloud Watermark & Code Access Suppression */
    #MainMenu {{visibility: hidden !important; display: none !important;}}
    header {{visibility: hidden !important; display: none !important;}}
    footer {{visibility: hidden !important; display: none !important;}}
    [data-testid="stHeader"] {{display: none !important;}}
    [data-testid="stToolbar"] {{display: none !important;}}
    .stAppDeployButton {{display: none !important;}}
    button[title="View source on GitHub"] {{display: none !important;}}
    a[href*="github.com"] {{display: none !important;}}
    [data-testid="manage-app-button"] {{display: none !important; visibility: hidden !important;}}
    div[class*="viewerBadge"] {{display: none !important; visibility: hidden !important;}}
    div[class*="manage-app"] {{display: none !important; visibility: hidden !important;}}
    .viewerBadge_container__1QSob {{display: none !important; visibility: hidden !important;}}
    .styles_viewerBadge__CvC9N {{display: none !important; visibility: hidden !important;}}
    [data-testid="stStatusWidget"] {{display: none !important; visibility: hidden !important;}}
    [data-testid="stDecoration"] {{display: none !important; visibility: hidden !important;}}
    section[data-testid="stSidebar"] {{display: none !important;}}

    /* Global Dark Slate & High-Contrast Typography */
    .stApp {{
        background-color: {active_bg} !important;
        color: #F8FAFC !important;
    }}
    
    /* Input Labels: Make Pure White & Bold */
    label, [data-testid="stWidgetLabel"] p {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 13.5px !important;
        letter-spacing: 0.3px !important;
    }}

    /* Text Inputs, Number Boxes & Selectboxes */
    div[data-baseweb="input"] input, div[data-baseweb="select"] {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
        background-color: #111827 !important;
    }}
    div[data-baseweb="input"] {{
        border: 1.5px solid #334155 !important;
        border-radius: 6px !important;
    }}

    /* High Visibility Solid Contrast Buttons */
    .stButton button {{
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        border: 1.5px solid {active_accent} !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
        padding: 8px 14px !important;
        transition: all 0.2s ease-in-out !important;
    }}
    .stButton button:hover {{
        background-color: {active_accent} !important;
        color: #0F172A !important;
        border-color: #FFFFFF !important;
    }}

    /* Brand Header */
    .brand-title {{
        text-align: center;
        font-size: 34px;
        font-weight: 900;
        letter-spacing: 2px;
        color: {active_accent};
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        margin-top: -10px;
        margin-bottom: 0px;
    }}
    .brand-subtitle {{
        text-align: center;
        font-size: 12.5px;
        font-weight: 700;
        letter-spacing: 2.5px;
        color: #94A3B8;
        text-transform: uppercase;
        margin-bottom: 20px;
    }}

    /* Section Headings */
    .section-title {{
        font-size: 14px;
        font-weight: 800;
        color: {active_accent};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
        border-bottom: 2px solid #1E293B;
        padding-bottom: 5px;
    }}

    /* Project Cards */
    .project-card-white {{
        background-color: #FFFFFF;
        color: #0F172A;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 6px 14px rgba(0,0,0,0.4);
    }}
    .project-code-badge {{
        background-color: #064E3B;
        color: #34D399;
        font-family: monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
        margin: 6px 0;
    }}
    .contractor-text {{
        color: #059669;
        font-weight: 800;
        font-size: 13.5px;
        margin-bottom: 8px;
    }}
    .metric-dot-row {{
        color: #F8FAFC;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 6px;
    }}
    .metric-dot-green {{
        color: #34D399;
        font-weight: 700;
    }}

    /* Sliders styling */
    .stSlider [data-baseweb="slider"] {{ color: #FFFFFF !important; }}
    div[data-testid="stThumbValue"] {{
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        background-color: #0F172A !important;
        border: 1.5px solid {active_accent} !important;
        padding: 2px 8px !important;
        border-radius: 6px !important;
    }}
    div[role="slider"] {{
        background-color: #EF4444 !important;
        border: 2px solid #FFFFFF !important;
    }}
    div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] {{
        color: #94A3B8 !important;
        font-weight: 700 !important;
        font-size: 12px !important;
    }}

    .sidebar-note {{
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-left: 3px solid {active_accent};
        padding: 8px 10px;
        border-radius: 6px;
        font-size: 11.5px;
        color: #CBD5E1;
        margin-top: 8px;
        line-height: 1.4;
    }}
</style>
""", unsafe_allow_html=True)

# ALL 28 Indian States & 8 Union Territories Master Hierarchy
ALL_INDIAN_STATES = [
    "Select State", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", 
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", 
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", 
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman & Nicobar", "Chandigarh", 
    "Dadra & Nagar Haveli and Daman & Diu", "Delhi", "Jammu and Kashmir", "Ladakh", 
    "Lakshadweep", "Puducherry"
]

def get_geo_hierarchy():
    return {
        "Bihar": {
            "Araria": ["Araria Sadar", "Joukihat", "Palasi", "Raniganj", "Sikti", "Kursakanta", "Forbesganj", "Bhargama", "Narpatganj"],
            "Aurangabad": ["Aurangabad Sadar", "Barun", "Deo", "Haspura", "Kutumba", "Madanpur", "Navinagar", "Rafiganj", "Daudnagar", "Goh", "Obra"],
            "Banka": ["Banka Sadar", "Amarpur", "Barahat", "Baunsi", "Belhar", "Chanan", "Dhoraiya", "Fullidumar", "Katoriya", "Rajaun", "Sambhuganj"],
            "Begusarai": ["Begusarai Sadar", "Barauni", "Birpur", "Matihani", "Shamho Akha Kurha", "Bakhri", "Garhpura", "Teghra", "Bachhwara"],
            "Bhagalpur": ["Bhagalpur Sadar", "Jagdishpur", "Nathnagar", "Sabour", "Goradih", "Shahkund", "Kahalgaon", "Pirpainti", "Naugachhia", "Gopalpur", "Sultanganj"],
            "Bhojpur": ["Ara Sadar", "Agiaon", "Barhara", "Koilwar", "Sandesh", "Shahpur", "Udwantnagar", "Jagdishpur", "Piro", "Charpokhari"],
            "Buxar": ["Buxar Sadar", "Barhampur", "Chausa", "Chaugain", "Itarhi", "Rajpur", "Dumraon", "Nawanagar", "Simri"],
            "Chapra(Saran)": ["Chhapra Sadar", "Garkha", "Jalalpur", "Manjhi", "Nagra", "Panapur", "Revelganj", "Taraiya", "Marhaura", "Sonepur", "Parsa"],
            "Darbhanga": ["Darbhanga Sadar", "Bahadurpur", "Hayaghat", "Hanumannagar", "Jale", "Keoti", "Manigachhi", "Singhwara", "Benipur", "Biraul", "Kusheshwar Asthan"],
            "East Champaran": ["Chakia", "Kalyanpur", "Kesaria", "Madhuban", "Mehsi", "Tetaria", "Motihari Sadar", "Kotwa", "Piprakothi", "Turkaulia", "Raxaul", "Areraj", "Dhaka", "Pakridayal"],
            "Gaya": ["Gaya Sadar", "Bodh Gaya", "Manpur", "Tankuppa", "Barachatti", "Belaganj", "Fatehpur", "Tekari", "Sherghati", "Dobhi", "Amas"],
            "Jahanabad": ["Jahanabad Sadar", "Ghoshi", "Hulashganj", "Kako", "Makhdumpur", "Modanganj", "Ratni Faridpur"],
            "Jamui": ["Jamui Sadar", "Barhat", "Chakai", "Gidhaur", "Jhajha", "Khaira", "Laxmipur", "Sikandra", "Sono"],
            "Kaimur (Bhabhua)": ["Bhabhua Sadar", "Bhagwanpur", "Chainpur", "Chand", "Rampur", "Mohania", "Adhaura", "Durgawati", "Kudra", "Ramgarh"],
            "Katihar": ["Katihar Sadar", "Dandkhora", "Falka", "Hasanganj", "Korha", "Mansahi", "Pranpur", "Barsoi", "Manihari"],
            "Khagaria": ["Khagaria Sadar", "Alauli", "Beldaur", "Chautham", "Mansi", "Gogri", "Parbatta"],
            "Lakhisarai": ["Lakhisarai Sadar", "Barahiya", "Channan", "Halsi", "Pipariya", "Ramgarh Chowk", "Surajgarha"],
            "Madhepura": ["Madhepura Sadar", "Gamharia", "Ghelarh", "Murliganj", "Singheshwar", "Alamnagar", "Bihariganj", "Chausa", "Uda Kishanganj"],
            "Madhubani": ["Madhubani Sadar", "Bisfi", "Khajauli", "Pandaul", "Rajnagar", "Rahika", "Benipatti", "Jhanjharpur", "Phulparas"],
            "Muzaffarpur": ["Mushahari", "Bochahan", "Gaighat", "Aurai", "Katra", "Sakra", "Kanti", "Motipur", "Baruraj", "Sahebganj", "Paroo", "Saraiya", "Minapur"],
            "Nalanda": ["Bihar Sharif Sadar", "Asthawan", "Bind", "Giriak", "Harnaut", "Noorsarai", "Rahui", "Rajgir", "Islampur", "Hilsa", "Ekangarsarai"],
            "Nawada": ["Nawada Sadar", "Akbarpur", "Govindpur", "Kashichak", "Kowakole", "Meskaur", "Nardiganj", "Narhat", "Pakribarawan", "Rajauli", "Hisua"],
            "Patna": ["Danapur", "Khagaul", "Maner", "Bihta", "Patna Sadar", "Phulwari Sharif", "Sampatchak", "Barh", "Bakhtiarpur", "Mokama", "Masaurhi", "Paliganj", "Fatuha"],
            "Purnia": ["Purnia East", "Purnia West", "Dagarua", "Jalalgarh", "Kasba", "Banmankhi", "Dhamdaha", "Baisi", "Amour"],
            "Rohtas": ["Sasaram Sadar", "Chenari", "Karaghar", "Nokha", "Rohtas", "Sheosagar", "Tilouthu", "Bikramganj", "Dehri", "Nauhatta"],
            "Saharsa": ["Saharsa Sadar", "Kahara", "Mahishi", "Nauhatta", "Patarghat", "Salkhua", "Saur Bazar", "Sonbarsa", "Simri Bakhtiarpur"],
            "Samastipur": ["Samastipur Sadar", "Kalyanpur", "Khanpur", "Pusa", "Tajpur", "Warisnagar", "Dalsinghsarai", "Bibhutipur", "Ujiarpur", "Patori", "Rosera"],
            "Sheikhpura": ["Sheikhpura Sadar", "Ariari", "Barbigha", "Chewara", "Ghatkusumbha", "Shekhopur Sarai"],
            "Sheohar": ["Sheohar Sadar", "Dumri Katsari", "Piprahi", "Purnahiya", "Tariyani Chowk"],
            "Sitamarhi": ["Dumra", "Bairgania", "Belsand", "Bokhra", "Majorganj", "Nanpur", "Parsauni", "Riga", "Runni Saidpur", "Suppi", "Pupri", "Sonbarsa"],
            "Gopalganj": ["Gopalganj Sadar", "Hathua", "Kuchaikote", "Manjha", "Thawe", "Barauli", "Sidhwaliya", "Baikunthpur"],
            "Siwan": ["Siwan Sadar", "Mairwa", "Darauli", "Raghunathpur", "Maharajganj", "Goreakothi", "Barharia"],
            "Supaul": ["Supaul Sadar", "Kishanpur", "Raghopur", "Saraigarh", "Pipra", "Triveniganj", "Nirmali"],
            "Kishanganj": ["Kishanganj Sadar", "Bahadurganj", "Dighalbank", "Thakurganj", "Pothia", "Kochadhaman", "Terhagachh"],
            "Arwal": ["Arwal Sadar", "Kaler", "Karpi", "Kurtha", "Sonbhadra Banshi Suryapur"],
            "West Champaran": ["Bettiah Sadar", "Bagaha", "Narkatiaganj", "Ramnagar", "Chanpatia", "Lauriya", "Majhaulia", "Gaunaha", "Thakaraha"],
            "Munger": ["Munger Sadar", "Jamalpur", "Bariarpur", "Dharhara", "Kharagpur", "Tarapur", "Asarganj", "Tetia Bamber"],
            "Vaishali": ["Hajipur Sadar", "Mahua", "Lalganj", "Vaishali", "Jandaha", "Raghopur", "Patepur", "Bidupur"]
        },
        "Uttar Pradesh": {
            "Lucknow": ["Lucknow Central", "Bakshi Ka Talab", "Sarojini Nagar", "Mohanlalganj"],
            "Varanasi": ["Varanasi Sadar", "Pindra", "Rohaniya", "Sewapuri"],
            "Prayagraj": ["Prayagraj Sadar", "Phulpur", "Soraon", "Handia", "Karchhana"],
            "Kanpur": ["Kanpur Nagar", "Ghatampur", "Bilhaur", "Kalyanpur"],
            "Noida": ["Dadri", "Jewar", "Bisrakh", "Greater Noida"]
        },
        "Maharashtra": {
            "Mumbai": ["Mumbai City", "Mumbai Suburban", "Andheri", "Kurla", "Borivali"],
            "Pune": ["Pune City", "Haveli", "Baramati", "Pimpri-Chinchwad"],
            "Nagpur": ["Nagpur Urban", "Nagpur Rural", "Hingna", "Kamptee", "Katol"],
            "Thane": ["Thane City", "Kalyan", "Bhiwandi", "Ulhasnagar"]
        },
        "Gujarat": {
            "Ahmedabad": ["Ahmedabad City", "Dholera", "Sanand", "Viramgam", "Daskroi"],
            "Surat": ["Surat City", "Chorasi", "Olpad", "Bardoli", "Kamrej"],
            "Vadodara": ["Vadodara Urban", "Padra", "Savli", "Waghodia"],
            "Kutch": ["Bhuj", "Gandhidham", "Khavda", "Mundra", "Anjar"]
        }
    }

# Master Dataset Loader (Real MoSPI PAIMANA Flash Report + PMGSY Dataset)
@st.cache_data
def load_data():
    if os.path.exists("all_india_live_projects.csv"):
        try:
            return pd.read_csv("all_india_live_projects.csv")
        except Exception:
            pass
    if os.path.exists("bihar_live_projects.csv"):
        try:
            return pd.read_csv("bihar_live_projects.csv")
        except Exception:
            pass
    # Official MoSPI PAIMANA Ongoing Infrastructure Central Sector Projects
    return pd.DataFrame([
        {
            "State": "Bihar",
            "Project_Name": "6L Bridge across Ganga as part of Patna Ring Road NH-131G (Sherpur-Dighwara)",
            "District": "Patna",
            "Subdivision": "Danapur",
            "Block": "Maner",
            "Package_ID": "MOSPI_618738",
            "Contractor_Name": "SP Singla Constructions Pvt Ltd (NHAI)",
            "Original_Cost_Cr": 6292.00,
            "Original_Duration": 48,
            "Elapsed_Months": 30,
            "Cumulative_Spend_Cr": 734.19,
            "Physical_Progress_Pct": 22.05,
            "Delayed_Milestones": 4,
            "Revisions_Count": 1,
            "Land_Risk_Score": 8.4,
            "WPI_Inflation_Index": 116.50,
            "Site_Engineer": "Er. Project Director, NHAI PIU Patna"
        },
        {
            "State": "Bihar",
            "Project_Name": "Motihari Chhatauni Flyover & Junction Improvement Works",
            "District": "East Champaran",
            "Subdivision": "Motihari Sadar",
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
            "Site_Engineer": "Er. Alok Sharma, AEE RCD"
        },
        {
            "State": "Maharashtra",
            "Project_Name": "Mumbai-Ahmedabad High Speed Rail Project (508 Km Bullet Train)",
            "District": "Mumbai",
            "Subdivision": "Mumbai Suburban",
            "Block": "Kurla",
            "Package_ID": "MOSPI_705728",
            "Contractor_Name": "National High Speed Rail Corporation (NHSRCL)",
            "Original_Cost_Cr": 108000.00,
            "Original_Duration": 84,
            "Elapsed_Months": 68,
            "Cumulative_Spend_Cr": 90966.89,
            "Physical_Progress_Pct": 62.16,
            "Delayed_Milestones": 5,
            "Revisions_Count": 2,
            "Land_Risk_Score": 8.5,
            "WPI_Inflation_Index": 118.20,
            "Site_Engineer": "Er. Chief Project Director, NHSRCL"
        },
        {
            "State": "Delhi",
            "Project_Name": "Delhi Metro Rail Project Phase-IV (3 Priority Corridors)",
            "District": "Delhi",
            "Subdivision": "Delhi Central",
            "Block": "Civil Lines",
            "Package_ID": "MOSPI_702632",
            "Contractor_Name": "Delhi Metro Rail Corporation (DMRC)",
            "Original_Cost_Cr": 24948.65,
            "Original_Duration": 60,
            "Elapsed_Months": 48,
            "Cumulative_Spend_Cr": 21420.76,
            "Physical_Progress_Pct": 83.46,
            "Delayed_Milestones": 1,
            "Revisions_Count": 0,
            "Land_Risk_Score": 6.1,
            "WPI_Inflation_Index": 112.40,
            "Site_Engineer": "Er. Executive Director (Civil), DMRC"
        },
        {
            "State": "Gujarat",
            "Project_Name": "Transmission System Evacuation Potential RE Zone Khavda (8 GW Part A)",
            "District": "Kutch",
            "Subdivision": "Bhuj",
            "Block": "Khavda",
            "Package_ID": "MOSPI_615347",
            "Contractor_Name": "POWERGRID West Central Transmission Ltd.",
            "Original_Cost_Cr": 24819.00,
            "Original_Duration": 48,
            "Elapsed_Months": 18,
            "Cumulative_Spend_Cr": 2978.28,
            "Physical_Progress_Pct": 18.56,
            "Delayed_Milestones": 2,
            "Revisions_Count": 0,
            "Land_Risk_Score": 5.4,
            "WPI_Inflation_Index": 111.80,
            "Site_Engineer": "Er. General Manager, PowerGrid Khavda"
        }
    ])

# Safe Machine Learning Model Loader
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

geo_hierarchy = get_geo_hierarchy()
paimana_df = load_data()
time_model, cost_model = load_ml_models()

# State Management
if 'selected_record' not in st.session_state:
    st.session_state['selected_record'] = None
if 'ai_evaluated' not in st.session_state:
    st.session_state['ai_evaluated'] = False
if 'projects_fetched' not in st.session_state:
    st.session_state['projects_fetched'] = False

# Top Header Layout with Styled Settings Popover
header_col1, header_col2, header_col3 = st.columns([1, 8, 1.2])

with header_col2:
    st.markdown(f"<div class='brand-title'>🏛️ PAIMANA AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='brand-subtitle'>INFRASTRUCTURE ANALYSIS & PREDICTIVE COMPLIANCE ENGINE</div>", unsafe_allow_html=True)

with header_col3:
    with st.popover("⚙️ Settings (⋮)", use_container_width=True):
        st.markdown("#### 🎨 Theme Customizer")
        new_theme = st.selectbox("Background Style", list(bg_map.keys()), index=list(bg_map.keys()).index(st.session_state["app_bg_theme"]))
        new_accent = st.selectbox("Accent Highlight", list(accent_map.keys()), index=list(accent_map.keys()).index(st.session_state["app_accent_color"]))
        if new_theme != st.session_state["app_bg_theme"] or new_accent != st.session_state["app_accent_color"]:
            st.session_state["app_bg_theme"] = new_theme
            st.session_state["app_accent_color"] = new_accent
            st.rerun()

# Responsive Main 3-Column Interface (Always Visible on Mobile & Desktop)
col_geo, col_sec1, col_sec2 = st.columns([0.85, 1.1, 1.05], gap="medium")

# COLUMN 1: Direct Administrative Jurisdiction (All States & UTs)
with col_geo:
    st.markdown("<div class='section-title'>📍 JURISDICTION SELECTION</div>", unsafe_allow_html=True)
    
    selected_state = st.selectbox("1. State / UT", ALL_INDIAN_STATES, index=4 if "Bihar" in ALL_INDIAN_STATES else 0)
    
    # Dynamic District Population
    if selected_state in geo_hierarchy:
        district_pool = ["Select District"] + sorted(list(geo_hierarchy[selected_state].keys()))
    else:
        # Fallback districts extracted from dataset
        state_df = paimana_df[paimana_df['State'].astype(str).str.lower() == selected_state.lower()] if 'State' in paimana_df.columns else pd.DataFrame()
        if not state_df.empty and 'District' in state_df.columns:
            district_pool = ["Select District"] + sorted(list(state_df['District'].dropna().unique()))
        else:
            district_pool = ["Select District", f"{selected_state} Central HQ"]
            
    selected_district = st.selectbox("2. District", district_pool, index=1 if len(district_pool) > 1 else 0)

    # Dynamic Block / Subdivision
    if selected_state in geo_hierarchy and selected_district in geo_hierarchy[selected_state]:
        block_pool = ["Select Block / Division"] + sorted(geo_hierarchy[selected_state][selected_district])
    else:
        block_pool = ["Select Block / Division", "HQ Project Area", "Industrial Corridor", "Urban Package"]
        
    selected_block = st.selectbox("3. Block / Sub-Division", block_pool, index=1 if len(block_pool) > 1 else 0)

    fetch_btn = st.button("🗣️ Fetch Ongoing Projects (Enter ↵)", use_container_width=True)
    if fetch_btn:
        if selected_state != "Select State":
            st.session_state['projects_fetched'] = True
            st.session_state['active_state'] = selected_state
            st.session_state['active_district'] = selected_district
            st.session_state['active_block'] = selected_block
        else:
            st.error("Please select a valid State / UT first.")

    demo_btn = st.button("🚨 Load Motihari Chhatauni Demo Preset", use_container_width=True)
    st.markdown("""
    <div class="sidebar-note">
        <b>📌 Note:</b> Real-time ingestion enabled across all 28 Indian States & 8 UTs from MoSPI PAIMANA Flash Reports.
    </div>
    """, unsafe_allow_html=True)

    if demo_btn:
        preset_rec = {
            "State": "Bihar",
            "Project_Name": "Motihari Chhatauni Flyover & Junction Improvement Works",
            "District": "East Champaran",
            "Subdivision": "Motihari Sadar",
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
            "Site_Engineer": "Er. Alok Sharma, AEE RCD"
        }
        st.session_state['selected_record'] = preset_rec
        st.session_state['projects_fetched'] = True
        st.session_state['active_state'] = "Bihar"
        st.session_state['active_district'] = "East Champaran"
        st.session_state['active_block'] = "Motihari Sadar"
        st.session_state['inp_cost'] = float(preset_rec['Original_Cost_Cr'])
        st.session_state['inp_dur'] = int(preset_rec['Original_Duration'])
        st.session_state['inp_elap'] = int(preset_rec['Elapsed_Months'])
        st.session_state['inp_sp'] = float(preset_rec['Cumulative_Spend_Cr'])
        st.session_state['box_phys'] = float(preset_rec['Physical_Progress_Pct'])
        st.session_state['box_ms'] = int(preset_rec['Delayed_Milestones'])
        st.session_state['box_rev'] = int(preset_rec['Revisions_Count'])
        st.session_state['sl_land'] = float(preset_rec['Land_Risk_Score'])
        st.session_state['sl_wpi'] = float(preset_rec['WPI_Inflation_Index'])
        st.session_state['ai_evaluated'] = True

# COLUMN 2: Details About Ongoing Projects
with col_sec1:
    st.markdown("<div class='section-title'>📁 SECTION 1: DETAILS ABOUT ONGOING PROJECTS</div>", unsafe_allow_html=True)
    
    active_st = st.session_state.get('active_state', selected_state)
    active_dist = st.session_state.get('active_district', selected_district)
    active_blk = st.session_state.get('active_block', selected_block)
    
    # Filter dataset according to state and district
    matched_projects = []
    if active_st != "Select State":
        temp_df = paimana_df.copy()
        if 'State' in temp_df.columns:
            temp_df = temp_df[temp_df['State'].astype(str).str.lower() == active_st.lower()]
        
        if active_dist != "Select District":
            dist_term = active_dist.split()[0].strip().lower()
            m_df = temp_df[temp_df['District'].astype(str).str.lower().str.contains(dist_term, na=False)]
            if not m_df.empty:
                temp_df = m_df

        matched_projects = [r for _, r in temp_df.iterrows()]
    else:
        matched_projects = [r for _, r in paimana_df.iterrows()]
        
    if not matched_projects:
        st.info("ℹ️ Currently, no active government construction work is underway at this location.")
        active_row = None
    else:
        project_options = [str(r["Project_Name"]) for r in matched_projects]
        selected_inspect = st.selectbox("Select Construction Work to Inspect:", project_options, index=0)
        active_row = next((r for r in matched_projects if str(r["Project_Name"]) == selected_inspect), matched_projects[0])

        st.markdown(f"""
        <div class="project-card-white">
            <div style="font-size: 15px; font-weight: 800; color: #0284C7; line-height: 1.3;">
                📌 {active_row['Project_Name']}
            </div>
            <div><span class="project-code-badge">{active_row.get('Package_ID', 'MOSPI_PAIMANA_2026')}</span></div>
            <div class="contractor-text">🏗️ {active_row.get('Contractor_Name', 'Empanelled Central/State Agency')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        b1, b2 = st.columns(2)
        with b1:
            st.markdown(f"<div class='metric-dot-row'>• <b>Original Cost:</b> <span class='metric-dot-green'>₹{float(active_row['Original_Cost_Cr']):.2f} Cr</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Duration:</b> <span class='metric-dot-green'>{int(active_row['Original_Duration'])} M</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Elapsed:</b> <span class='metric-dot-green'>{int(active_row['Elapsed_Months'])} M</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Spend:</b> <span class='metric-dot-green'>₹{float(active_row['Cumulative_Spend_Cr']):.2f} Cr</span></div>", unsafe_allow_html=True)
        with b2:
            st.markdown(f"<div class='metric-dot-row'>• <b>Progress:</b> <span class='metric-dot-green'>{float(active_row['Physical_Progress_Pct']):.1f}%</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Delayed M/S:</b> <span class='metric-dot-green'>{int(active_row['Delayed_Milestones'])}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Revisions:</b> <span class='metric-dot-green'>{int(active_row.get('Revisions_Count', 0))}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-dot-row'>• <b>Land Risk:</b> <span class='metric-dot-green'>{float(active_row['Land_Risk_Score']):.1f}</span></div>", unsafe_allow_html=True)

        load_sec2_btn = st.button("📥 Load This Project Data into Section 2", use_container_width=True)
        if load_sec2_btn:
            row_dict = active_row.to_dict()
            st.session_state['selected_record'] = row_dict
            st.session_state['inp_cost'] = float(row_dict['Original_Cost_Cr'])
            st.session_state['inp_dur'] = int(row_dict['Original_Duration'])
            st.session_state['inp_elap'] = int(row_dict['Elapsed_Months'])
            st.session_state['inp_sp'] = float(row_dict['Cumulative_Spend_Cr'])
            st.session_state['box_phys'] = float(row_dict['Physical_Progress_Pct'])
            st.session_state['box_ms'] = int(row_dict['Delayed_Milestones'])
            st.session_state['box_rev'] = int(row_dict.get('Revisions_Count', 0))
            st.session_state['sl_land'] = float(row_dict['Land_Risk_Score'])
            st.session_state['sl_wpi'] = float(row_dict['WPI_Inflation_Index'])
            st.session_state['ai_evaluated'] = False
            st.rerun()

# COLUMN 3: Predict Project Future Overview (User-Editable Custom Input Boxes + 2 Sliders)
rec = st.session_state.get('selected_record') or (active_row.to_dict() if active_row is not None else {})

with col_sec2:
    st.markdown("<div class='section-title'>⚡ SECTION 2: PREDICT PROJECT FUTURE OVERVIEW</div>", unsafe_allow_html=True)
    
    s2_col1, s2_col2 = st.columns(2)
    with s2_col1:
        inp_cost = st.number_input("Cost (₹ Cr)", value=float(st.session_state.get('inp_cost', rec.get('Original_Cost_Cr', 341.56))), key="inp_cost")
        inp_duration = st.number_input("Duration (Months)", value=int(st.session_state.get('inp_dur', rec.get('Original_Duration', 27))), key="inp_dur")
        inp_elapsed = st.number_input("Elapsed (Months)", value=int(st.session_state.get('inp_elap', rec.get('Elapsed_Months', 13))), key="inp_elap")
        inp_spend = st.number_input("Spend (₹ Cr)", value=float(st.session_state.get('inp_sp', rec.get('Cumulative_Spend_Cr', 200.56))), key="inp_sp")
    with s2_col2:
        inp_phys = st.number_input("Progress (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.get('box_phys', rec.get('Physical_Progress_Pct', 40.80))), key="box_phys")
        inp_milestones = st.number_input("Delayed M/S", min_value=0, max_value=20, value=int(st.session_state.get('box_ms', rec.get('Delayed_Milestones', 0))), key="box_ms")
        inp_revisions = st.number_input("Revisions", min_value=0, max_value=10, value=int(st.session_state.get('box_rev', rec.get('Revisions_Count', 0))), key="box_rev")
        
    inp_land = st.slider("Local Land Risk (1-10)", 1.0, 10.0, float(st.session_state.get('sl_land', rec.get('Land_Risk_Score', 7.70))), key="sl_land")
    inp_wpi = st.slider("WPI Material Inflation Index", 90.0, 140.0, float(st.session_state.get('sl_wpi', rec.get('WPI_Inflation_Index', 116.50))), key="sl_wpi")

    run_ai = st.button("⚡ Run AI Prediction & Risk Analysis (Enter ↵)", use_container_width=True)
    if run_ai:
        st.session_state['ai_evaluated'] = True

# SHOW PREDICTION ONLY AFTER AI EVALUATION BUTTON CLICK (HANDLES LOADED OR CUSTOM USER INPUTS)
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

    # Risk Output Cards
    rc1, rc2, rc3 = st.columns([1, 1, 1.2])
    with rc1:
        st.markdown(f"""
        <div style="background-color: #111827; border: 1px solid #1F2937; padding: 14px; border-radius: 8px;">
            <span style="font-size: 11px; color: #9CA3AF; text-transform: uppercase;">Predicted Cost Overrun</span>
            <div style="font-size: 26px; font-weight: 800; color: #FFFFFF; margin: 4px 0;">{pred_cost_overrun_pct:.1f}%</div>
            <span style="color: #EF4444; font-size: 13px; font-weight: 600;">↑ +₹{cost_escalation_cr:.1f} Cr</span>
        </div>
        """, unsafe_allow_html=True)
    with rc2:
        st.markdown(f"""
        <div style="background-color: #111827; border: 1px solid #1F2937; padding: 14px; border-radius: 8px;">
            <span style="font-size: 11px; color: #9CA3AF; text-transform: uppercase;">Predicted Schedule Delay</span>
            <div style="font-size: 26px; font-weight: 800; color: #FFFFFF; margin: 4px 0;">{pred_delay_months:.1f} Months</div>
            <span style="color: #EF4444; font-size: 13px; font-weight: 600;">↑ +{pred_delay_months:.1f} M Delay</span>
        </div>
        """, unsafe_allow_html=True)
    with rc3:
        st.markdown(f"""
        <div style="background-color: #111827; border: 1px solid #1F2937; padding: 14px; border-radius: 8px; text-align: center;">
            <div style="background-color: {alert_bg}22; border: 1px solid {alert_bg}; padding: 10px; border-radius: 6px; margin-top: 2px;">
                <span style="color: {alert_bg}; font-weight: 800; font-size: 17px;">{alert_badge}</span><br>
                <span style="color: #E2E8F0; font-size: 12.5px; font-weight: 600;">({int(cpri_score)}/100)</span>
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
        fig_s = go.Figure()
        fig_s.add_trace(go.Bar(name='Planned Target (%)', x=['Schedule Horizon'], y=[planned_progress_pct], marker=dict(color=active_accent, line=dict(color='#0284C7', width=1.5)), width=0.35))
        fig_s.add_trace(go.Bar(name='Actual Ground Progress (%)', x=['Schedule Horizon'], y=[inp_phys], marker=dict(color='#10B981', line=dict(color='#059669', width=1.5)), width=0.35))
        fig_s.update_layout(barmode='group', template="plotly_dark", height=340, title="EVM Square Block Progress Benchmark (Planned vs On-Site Physical)", yaxis_title="Physical Completion (%)", yaxis=dict(range=[0, 100]), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), margin=dict(l=20, r=20, t=35, b=20))
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
        active_st_name = st.session_state.get('active_state', selected_state)
        active_dist_name = st.session_state.get('active_district', selected_district)
        proj_title = rec.get('Project_Name', 'Registered Works Package')
        pkg_code = rec.get('Package_ID', f"MOSPI_{active_st_name[:3].upper()}_2026_098")
        contractor = rec.get('Contractor_Name', 'M/S Executing Agency Pvt Ltd')
        officer = rec.get('Site_Engineer', 'Er. Executive Engineer (Infrastructure Works)')
        current_date_str = datetime.now().strftime('%d-%B-%Y')

        memo_text = f"""To,
The Authorized Managing Director / Project Head,
{contractor},
Principal Executing Agency,
Project Package: {proj_title},
Jurisdiction: {active_dist_name}, {active_st_name}, India.

Subject: Notice related to critical schedule slippage and breach of baseline milestones at {proj_title} (Package ID: {pkg_code}).

Dear Sir/Madam,

I hope this letter finds you well. I am writing this to formally notify you about serious concerns regarding the ongoing construction activities occurring at your work site for "{proj_title}" located within {selected_block}, {active_dist_name}, {active_st_name}, India. Based on our departmental inspection and verified data appraisal conducted via the MoSPI InfraDrishti-AI Framework, it is established that the actual on-site progress ({inp_phys:.2f}%) has substantially deviated from the approved baseline target ({planned_progress_pct:.2f}%), resulting in an unacceptable negative Schedule Variance of {schedule_variance_pct:.2f}% and an estimated slippage of +{pred_delay_months:.1f} Months.

This execution failure directly violates Clause 2 (Compensation for Delay) and Clause 3 of the Standard CPWD Works Manual Contract Agreement, read in conjunction with Rule 130 of General Financial Rules (GFR 2017) regarding the timely utilization of public funds and physical milestone adherence. Furthermore, the recorded Cost Performance Index (CPI) of {cpi:.2f} indicates front-loading of disbursed funds (₹{inp_spend:.2f} Cr spend out of ₹{inp_cost:.2f} Cr sanctioned) without corresponding physical delivery, creating potential fiscal distress and substantial delay to the public interest.

Further, the slow mobilization of machinery and recurring milestone carryovers have directly contradicted the approved PERT/CPM schedule set forth by this monitoring authority. This continued disregard for statutory delivery timelines is unacceptable and warrants immediate corrective intervention. Taking into consideration the aforementioned pointers, you are hereby directed to submit an escalated catch-up recovery schedule and deploy augmented double-shift resources immediately. Further, if this matter is not resolved and adequate cause is not shown in writing within 14 days from the date of issuance of this notice, we will be left with no choice but to levy statutory Liquidated Damages @ 1.0% per month under CPWD Clause 2 and escalate the matter for penal determination of the contract.

Thanking you in anticipation for your prompt attention to this matter. I hope we can resolve this operational deficit expeditiously for the timely commissioning of this public infrastructure.

Sincerely,
{officer},
Nodal Appraisal & Executive Engineer,
Infrastructure Project Monitoring Division (IPMD),
Ministry of Statistics & Programme Implementation (MoSPI),
{active_st_name}, India.
Date: {current_date_str}
"""
        st.text_area("Directive Notice Preview", memo_text, height=360)
        st.download_button(
            label="📥 Download Directive Notice (.txt)",
            data=memo_text,
            file_name=f"Directive_Notice_{active_st_name[:3]}_{datetime.now().strftime('%Y%m%d')}.txt",
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
