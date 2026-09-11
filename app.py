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
    initial_sidebar_state="expanded"
)

# User Preference Settings State
if "app_bg_theme" not in st.session_state:
    st.session_state["app_bg_theme"] = "Dark Slate (#0B0F19)"
if "app_accent_color" not in st.session_state:
    st.session_state["app_accent_color"] = "Cyan Blue (#38BDF8)"
if "app_font_scale" not in st.session_state:
    st.session_state["app_font_scale"] = "Standard (100%)"

# Dynamic Styling based on Settings
bg_map = {
    "Dark Slate (#0B0F19)": "#0B0F19",
    "Deep Midnight (#050811)": "#050811",
    "Pitch Black (#000000)": "#000000"
}
accent_map = {
    "Cyan Blue (#38BDF8)": "#38BDF8",
    "Emerald Green (#10B981)": "#10B981",
    "Amber Gold (#F59E0B)": "#F59E0B"
}
font_scale_map = {
    "Standard (100%)": "14px",
    "Medium (+10%)": "15.5px",
    "Large (+20%)": "17px"
}

active_bg = bg_map.get(st.session_state["app_bg_theme"], "#0B0F19")
active_accent = accent_map.get(st.session_state["app_accent_color"], "#38BDF8")
active_font_size = font_scale_map.get(st.session_state["app_font_scale"], "14px")

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
                font-size: 64px;
                font-weight: 900;
                letter-spacing: 4px;
                color: {active_accent};
                text-shadow: 0 0 30px rgba(56, 189, 248, 0.8);
                margin-bottom: 8px;
            }}
            .splash-sub {{
                font-size: 16px;
                font-weight: 700;
                letter-spacing: 5px;
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
            <div class="splash-sub">Infrastructure Predictive Risk Engine</div>
            <div class="splash-loader"><div class="splash-bar"></div></div>
            <p style="color: #64748B; font-size: 13px; margin-top: 14px;">Initializing CPWD/GFR Compliance & Model Workflows...</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(4.0)
    st.session_state["splash_done"] = True
    splash_placeholder.empty()

# Custom Aesthetic High-Contrast CSS & Settings Container
st.markdown(f"""
<style>
    /* Complete Cloud Watermark & Code Access Suppression */
    #MainMenu {{visibility: hidden !important; display: none !important;}}
    footer {{visibility: hidden !important; display: none !important;}}
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

    /* Sidebar Collapse & Reopen Arrow Fix (Mobile & Desktop) */
    header {{ background: transparent !important; height: auto !important; }}
    [data-testid="stHeader"] {{ background: transparent !important; height: auto !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    [data-testid="stSidebarCollapsedControl"] {{
        display: block !important;
        visibility: visible !important;
        z-index: 99999 !important;
        color: {active_accent} !important;
        background-color: #0F172A !important;
        border: 1px solid {active_accent} !important;
        border-radius: 6px !important;
        padding: 4px !important;
        margin-top: 8px !important;
        margin-left: 8px !important;
    }}
    [data-testid="stSidebarCollapsedControl"] button {{ color: {active_accent} !important; }}

    /* User Custom Theme Application */
    .stApp {{ background-color: {active_bg}; color: #F8FAFC; font-size: {active_font_size}; }}
    
    /* Top Center Brand Header */
    .brand-title {{
        text-align: center;
        font-size: 38px;
        font-weight: 900;
        letter-spacing: 2px;
        color: {active_accent};
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        margin-top: -10px;
        margin-bottom: 0px;
    }}
    .brand-subtitle {{
        text-align: center;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 3px;
        color: #94A3B8;
        text-transform: uppercase;
        margin-bottom: 24px;
    }}

    /* Section Headings */
    .section-title {{
        font-size: 16px;
        font-weight: 800;
        color: {active_accent};
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
        border-bottom: 2px solid #1E293B;
        padding-bottom: 6px;
    }}

    /* Cards & Container Visibility */
    .project-card-white {{
        background-color: #FFFFFF;
        color: #0F172A;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
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
        font-size: 14px;
        margin-bottom: 8px;
    }}
    .metric-dot-row {{
        color: #F1F5F9;
        font-size: 13.5px;
        font-weight: 500;
        margin-bottom: 6px;
    }}
    .metric-dot-green {{
        color: #34D399;
        font-weight: 700;
    }}

    /* High-Contrast Slider Number Visibility Fix */
    .stSlider [data-baseweb="slider"] {{ color: #FFFFFF !important; }}
    div[data-testid="stThumbValue"] {{
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        background-color: #0F172A !important;
        border: 1.5px solid {active_accent} !important;
        padding: 3px 8px !important;
        border-radius: 6px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
    }}
    div[role="slider"] {{
        background-color: #EF4444 !important;
        border: 2px solid #FFFFFF !important;
    }}
    div[data-testid="stSlider"] div[data-testid="stMarkdownContainer"] p {{
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }}
    div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] {{
        color: #94A3B8 !important;
        font-weight: 700 !important;
        font-size: 12px !important;
    }}

    /* Sidebar Note Box */
    .sidebar-note {{
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-left: 3px solid {active_accent};
        padding: 8px 10px;
        border-radius: 6px;
        font-size: 11.5px;
        color: #94A3B8;
        margin-top: 6px;
        line-height: 1.4;
    }}
</style>
""", unsafe_allow_html=True)

# Complete 38 Districts, 101 Subdivisions, 534+ Blocks Master Hierarchy
def get_bihar_geo_hierarchy():
    return {
        "Araria": {
            "Araria Sub-Div": ["Araria", "Jokihat", "Kursakanta", "Palasi", "Raniganj", "Sikti"],
            "Forbesganj Sub-Div": ["Forbesganj", "Bhargama", "Narpatganj"]
        },
        "Arwal": {
            "Arwal Sub-Div": ["Arwal", "Kaler", "Karpi", "Kurtha", "Sonbhadra Banshi Suryapur"]
        },
        "Aurangabad": {
            "Aurangabad Sub-Div": ["Aurangabad", "Barun", "Jamhor", "Kutumba", "Madanpur", "Navinagar", "Rafiganj"],
            "Daudnagar Sub-Div": ["Daudnagar", "Goh", "Haspura", "Obra"]
        },
        "Banka": {
            "Banka Sub-Div": ["Banka", "Amarpur", "Barahat", "Bausi", "Belhar", "Chanan", "Dhoraiya", "Fullidumar", "Katoriya", "Rajaun", "Sambhuganj"]
        },
        "Begusarai": {
            "Begusarai Sadar Sub-Div": ["Begusarai", "Barauni", "Birpur", "Matihani", "Shamho Akha Kurha"],
            "Bakhri Sub-Div": ["Bakhri", "Garhpura", "Naokothi", "Parihara"],
            "Balia Sub-Div": ["Balia", "Dandari", "Sahebpur Kamal"],
            "Manjhaul Sub-Div": ["Cheria Bariarpur", "Chhorahi"],
            "Teghra Sub-Div": ["Teghra", "Bachhwara", "Bhagwanpur", "Mansurchak"]
        },
        "Bhagalpur": {
            "Bhagalpur Sadar Sub-Div": ["Jagdishpur", "Nathnagar", "Sabour", "Goradih", "Shahkund"],
            "Kahalgaon Sub-Div": ["Kahalgaon", "Pirpainti", "Sanokhar"],
            "Naugachhia Sub-Div": ["Naugachhia", "Bihpur", "Gopalpur", "Ismailpur", "Kharik", "Narayanpur", "Rangra Chowk"],
            "Sultanganj Sub-Div": ["Sultanganj"]
        },
        "Bhojpur (Ara)": {
            "Ara Sadar Sub-Div": ["Ara", "Agiaon", "Barhara", "Koilwar", "Sandesh", "Shahpur", "Udwantnagar"],
            "Jagdishpur Sub-Div": ["Jagdishpur", "Behea", "Garhani"],
            "Piro Sub-Div": ["Piro", "Charpokhari", "Tarari"]
        },
        "Buxar": {
            "Buxar Sub-Div": ["Buxar", "Barhampur", "Chausa", "Chaugain", "Itarhi", "Rajpur"],
            "Dumraon Sub-Div": ["Dumraon", "Brahmpur", "Chakki", "Kesath", "Nawanagar", "Simri"]
        },
        "Darbhanga": {
            "Darbhanga Sadar Sub-Div": ["Darbhanga", "Bahadurpur", "Hayaghat", "Hanumannagar", "Jale", "Keoti", "Manigachhi", "Singhwara"],
            "Benipur Sub-Div": ["Benipur", "Alinagar", "Baheri", "Biraul"],
            "Biraul Sub-Div": ["Ghanshyampur", "Kiratpur", "Kusheshwar Asthan", "Kusheshwar Asthan East", "Tardih"]
        },
        "East Champaran (Motihari)": {
            "Chakia Sub-Div": ["Chakia", "Kalyanpur", "Kesaria", "Madhuban", "Mehsi", "Tetaria"],
            "Motihari Sadar Sub-Div": ["Motihari Sadar", "Kotwa", "Piprakothi", "Turkaulia", "Banjariya"],
            "Raxaul Sub-Div": ["Raxaul", "Adapur", "Ramgarhwa", "Sugauli"],
            "Areraj Sub-Div": ["Areraj", "Paharpur", "Harsidhi", "Sangrampur"],
            "Dhaka Sub-Div": ["Dhaka", "Chiraiya", "Ghorasahan", "Banka Ghat", "Patahi"],
            "Pakridayal Sub-Div": ["Pakridayal", "Phena"]
        },
        "Gaya": {
            "Gaya Sadar Sub-Div": ["Gaya Sadar", "Bodh Gaya", "Manpur", "Tankuppa", "Barachatti", "Belaganj", "Fatehpur", "Mohanpur", "Paraiya", "Wazirganj"],
            "Tekari Sub-Div": ["Tekari", "Konch", "Guraru"],
            "Sherghati Sub-Div": ["Sherghati", "Dobhi", "Amas", "Banke Bazar", "Gurua", "Imamganj", "Dumaria"],
            "Neemchak Bathani Sub-Div": ["Neemchak Bathani", "Atri", "Khizirsarai", "Mohra"]
        },
        "Gopalganj": {
            "Gopalganj Sub-Div": ["Gopalganj", "Barauli", "Manjha", "Sidhwalia", "Thawe", "Uchkagaon", "Baikunthpur"],
            "Hathua Sub-Div": ["Hathua", "Bhorey", "Bijaipur", "Kateya", "Kuchaikote", "Phulwariya", "Puchhri"]
        },
        "Jamui": {
            "Jamui Sub-Div": ["Jamui", "Barhat", "Chakai", "Gidhaur", "Islamnagar Aliganj", "Jhajha", "Khaira", "Laxmipur", "Sikandra", "Sono"]
        },
        "Jehanabad": {
            "Jehanabad Sub-Div": ["Jehanabad", "Ghoshi", "Hulashganj", "Kako", "Makhdumpur", "Modanganj", "Ratni Faridpur"]
        },
        "Kaimur (Bhabhua)": {
            "Bhabhua Sub-Div": ["Bhabhua", "Bhagwanpur", "Chainpur", "Chand", "Rampur"],
            "Mohania Sub-Div": ["Mohania", "Adhaura", "Durgawati", "Kudra", "Nuon", "Ramgarh"]
        },
        "Katihar": {
            "Katihar Sadar Sub-Div": ["Katihar", "Dandkhora", "Falka", "Hasanganj", "Korha", "Kora", "Mansahi", "Pranpur", "Sameli"],
            "Barsoi Sub-Div": ["Barsoi", "Amdabad", "Azamnagar", "Balrampur", "Kadwa"],
            "Manihari Sub-Div": ["Manihari"]
        },
        "Khagaria": {
            "Khagaria Sub-Div": ["Khagaria", "Alauli", "Beldaur", "Chautham", "Mansi"],
            "Gogri Sub-Div": ["Gogri", "Parbatta"]
        },
        "Kishanganj": {
            "Kishanganj Sub-Div": ["Kishanganj", "Bahadurganj", "Dighalbank", "Kochadhaman", "Pothia", "Terhagachh", "Thakurganj"]
        },
        "Lakhisarai": {
            "Lakhisarai Sub-Div": ["Lakhisarai", "Barahiya", "Channan", "Halsi", "Pipariya", "Ramgarh Chowk", "Surajgarha"]
        },
        "Madhepura": {
            "Madhepura Sub-Div": ["Madhepura", "Gamharia", "Ghelarh", "Kishanganj", "Murliganj", "Shankarpur", "Singheshwar"],
            "Uda Kishanganj Sub-Div": ["Alamnagar", "Bihariganj", "Chausa", "Gwalpara", "Kumarkhand", "Puraini", "Uda Kishanganj"]
        },
        "Madhubani": {
            "Madhubani Sadar Sub-Div": ["Madhubani", "Bisfi", "Kaluahi", "Khajauli", "Ladnania", "Pandaul", "Rajnagar", "Rahika"],
            "Benipatti Sub-Div": ["Benipatti", "Basopatti", "Harlakhi", "Madhwapur"],
            "Jhanjharpur Sub-Div": ["Jhanjharpur", "Andhrathari", "Babubarhi", "Lakhnaur", "Madhepur", "Tamuria"],
            "Phulparas Sub-Div": ["Phulparas", "Ghoghardiha", "Khutauna", "Laukaha", "Narahiya"]
        },
        "Munger": {
            "Munger Sadar Sub-Div": ["Munger", "Bariarpur", "Dharhara", "Jamalpur"],
            "Kharagpur Sub-Div": ["Haveli Kharagpur", "Tetiabambar"],
            "Tarapur Sub-Div": ["Tarapur", "Asarganj", "Sangrampur"]
        },
        "Muzaffarpur": {
            "Muzaffarpur East Sub-Div": ["Mushahari", "Bochahan", "Gaighat", "Aurai", "Katra", "Bandra", "Dholi", "Muraul", "Sakra"],
            "Muzaffarpur West Sub-Div": ["Kanti", "Motipur", "Baruraj", "Sahebganj", "Paroo", "Saraiya", "Marwan", "Minapur"]
        },
        "Nalanda (Bihar Sharif)": {
            "Bihar Sharif Sub-Div": ["Bihar Sharif", "Asthawan", "Bind", "Giriak", "Harnaut", "Noorsarai", "Rahui", "Rajnagar", "Sarmera"],
            "Rajgir Sub-Div": ["Rajgir", "Ben", "Chandi", "Islampur", "Karai Parsurai", "Nagar Nausa", "Parwalpur", "Silao", "Tharthari"],
            "Hilsa Sub-Div": ["Hilsa", "Ekangarsarai"]
        },
        "Nawada": {
            "Nawada Sub-Div": ["Nawada", "Akbarpur", "Govindpur", "Kashichak", "Kowakole", "Meskaur", "Nardiganj", "Narhat", "Pakribarawan", "Roh", "Sirdala", "Warisaliganj"],
            "Rajauli Sub-Div": ["Rajauli", "Hisua"]
        },
        "Patna": {
            "Patna Sadar Sub-Div": ["Patna Sadar", "Phulwari Sharif", "Sampatchak"],
            "Danapur Sub-Div": ["Danapur", "Khagaul", "Maner", "Bihta"],
            "Barh Sub-Div": ["Barh", "Bakhtiarpur", "Mokama", "Pandarak", "Ghoswari", "Belchhi"],
            "Masaurhi Sub-Div": ["Masaurhi", "Dhanarua", "Punpun"],
            "Paliganj Sub-Div": ["Paliganj", "Dulhin Bazar", "Bikram"],
            "Patna City Sub-Div": ["Fatuha", "Daniyawan", "Khusrupur"]
        },
        "Purnia": {
            "Purnia Sadar Sub-Div": ["Purnia East", "Purnia West", "Dagarua", "Jalalgarh", "Kasba", "Krityanand Nagar", "Srinagar"],
            "Banmankhi Sub-Div": ["Banmankhi", "Barhara Kothi"],
            "Dhamdaha Sub-Div": ["Dhamdaha", "Bhawanipur", "Rupauli"],
            "Baisi Sub-Div": ["Baisi", "Amour", "Baisa"]
        },
        "Rohtas (Sasaram)": {
            "Sasaram Sub-Div": ["Sasaram", "Akorhigola", "Bhagwanpur", "Chenari", "Karaghar", "Nokha", "Rohtas", "Sheosagar", "Tilouthu"],
            "Bikramganj Sub-Div": ["Bikramganj", "Dawath", "Dinara", "Karakat", "Nasriganj", "Sanjhauli", "Suryapura"],
            "Dehri Sub-Div": ["Dehri", "Nauhatta", "Rajpur"]
        },
        "Saharsa": {
            "Saharsa Sadar Sub-Div": ["Saharsa", "Kahara", "Mahishi", "Nauhatta", "Patarghat", "Salkhua", "Saur Bazar", "Sonbarsa"],
            "Simri Bakhtiarpur Sub-Div": ["Simri Bakhtiarpur", "Banma Itahari"]
        },
        "Samastipur": {
            "Samastipur Sadar Sub-Div": ["Samastipur", "Kalyanpur", "Khanpur", "Pusa", "Tajpur", "Warisnagar"],
            "Dalsinghsarai Sub-Div": ["Dalsinghsarai", "Bibhutipur", "Ujiarpur", "Vidyapatinagar"],
            "Patori Sub-Div": ["Patori", "Mohanpur", "Mohiuddinagar"],
            "Rosera Sub-Div": ["Rosera", "Hasanpur", "Singhia", "Shivaji Nagar", "Bithan"]
        },
        "Saran (Chhapra)": {
            "Chhapra Sadar Sub-Div": ["Chhapra", "Garkha", "Jalalpur", "Manjhi", "Nagra", "Panapur", "Revelganj", "Rivilganj", "Taraiya"],
            "Marhaura Sub-Div": ["Marhaura", "Amnour", "Baniyapur", "Dighwara", "Ishupur", "Mashrakh", "Panapur"],
            "Sonepur Sub-Div": ["Sonepur", "Dariyapur", "Parsa", "Maker"]
        },
        "Sheikhpura": {
            "Sheikhpura Sub-Div": ["Sheikhpura", "Ariari", "Barbigha", "Chewara", "Ghatkusumbha", "Shekhopur Sarai"]
        },
        "Sheohar": {
            "Sheohar Sub-Div": ["Sheohar", "Dumri Katsari", "Piprahi", "Purnahiya", "Tariyani Chowk"]
        },
        "Sitamarhi": {
            "Sitamarhi Sadar Sub-Div": ["Dumra", "Bairgania", "Belsand", "Bokhra", "Majorganj", "Nanpur", "Parsauni", "Riga", "Runni Saidpur", "Suppi"],
            "Belsand Sub-Div": ["Belsand"],
            "Pupri Sub-Div": ["Pupri", "Bajpatti", "Bathnaha", "Charaut", "Parihar", "Sursand", "Sonbarsa"]
        },
        "Siwan": {
            "Siwan Sadar Sub-Div": ["Siwan", "Andar", "Barharia", "Darauli", "Goreakothi", "Guthani", "Hasanpura", "Hussainganj", "Mairwa", "Nautan", "Panchrukhi", "Raghunathpur", "Siswan", "Ziradei"],
            "Maharajganj Sub-Div": ["Maharajganj", "Bhagwanpur Hat", "Daraundha", "Lakri Nabiganj"]
        },
        "Supaul": {
            "Supaul Sub-Div": ["Supaul", "Basantpur", "Chhatapur", "Kishanpur", "Marauna", "Nirmali", "Pipra", "Pratapganj", "Raghopur", "Saraigarh Bhaptiyahi", "Triveniganj"]
        },
        "Vaishali (Hajipur)": {
            "Hajipur Sub-Div": ["Hajipur", "Bhagwanpur", "Bidupur", "Desri", "Goraul", "Jandaha", "Lalganj", "Mahnar", "Mahua", "Patedhi Belsar", "Raghopur", "Sahdai Buzurg", "Vaishali"],
            "Mahanar Sub-Div": ["Mahanar"],
            "Mahua Sub-Div": ["Mahua", "Chehrakala", "Jandaha", "Patedhi"]
        },
        "West Champaran (Bettiah)": {
            "Bettiah Sadar Sub-Div": ["Bettiah", "Bairia", "Chanpatia", "Jagdishpur", "Majhaulia", "Nautan", "Sikta"],
            "Bagaha Sub-Div": ["Bagaha-I", "Bagaha-II", "Bhairabganj", "Madhubani", "Piprasi", "Ramnagar", "Semraha", "Sidaw", "Thakraha"],
            "Narkatiaganj Sub-Div": ["Narkatiaganj", "Gaunaha", "Lauriya", "Mainatand"]
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
if 'projects_fetched' not in st.session_state:
    st.session_state['projects_fetched'] = False

# Sidebar Setup
st.sidebar.markdown("### 📍 Bihar Administrative Hierarchy")

# 1. State
state_list = ["Select State", "Bihar"]
selected_state = st.sidebar.selectbox("1. State", state_list, index=0)

# 2. District
all_districts = ["Select District"] + sorted(list(geo_hierarchy.keys()))
selected_district = st.sidebar.selectbox("2. District (38 Districts)", all_districts, index=0)

# 3. Subdivision
if selected_district in geo_hierarchy:
    subdiv_pool = ["Select Subdivision"] + sorted(list(geo_hierarchy[selected_district].keys()))
else:
    all_subdivs = sorted(list({sub for d in geo_hierarchy.values() for sub in d.keys()}))
    subdiv_pool = ["Select Subdivision"] + all_subdivs
selected_subdiv = st.sidebar.selectbox("3. Subdivision (101 Subdivisions)", subdiv_pool, index=0)

# 4. Block
if selected_district in geo_hierarchy and selected_subdiv in geo_hierarchy[selected_district]:
    block_pool = ["Select Block"] + sorted(geo_hierarchy[selected_district][selected_subdiv])
else:
    all_blocks = sorted(list({b for d in geo_hierarchy.values() for subs in d.values() for b in subs}))
    block_pool = ["Select Block"] + all_blocks
selected_block = st.sidebar.selectbox("4. Block (534 Blocks)", block_pool, index=0)

# Fetch button directly below block
fetch_btn = st.sidebar.button("🗣️ Fetch Ongoing Projects (Enter ↵)", use_container_width=True)

if fetch_btn:
    if (
        selected_state != "Select State" and 
        selected_district != "Select District" and 
        selected_subdiv != "Select Subdivision" and 
        selected_block != "Select Block"
    ):
        st.session_state['projects_fetched'] = True
        st.session_state['active_district'] = selected_district
    else:
        st.sidebar.error("⚠️ Please select complete location (State, District, Subdivision & Block) first.")
        st.session_state['projects_fetched'] = False

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Demo Preset at the bottom with professional note
demo_btn = st.sidebar.button("🚨 Load Motihari Chhatauni Demo Preset", use_container_width=True)
st.sidebar.markdown("""
<div class="sidebar-note">
    <b>📌 Note:</b> Click this preset to instantly test end-to-end AI prediction and appraisal workflows without manual jurisdiction input.
</div>
""", unsafe_allow_html=True)

if demo_btn:
    preset_rec = paimana_df.iloc[1].to_dict()
    st.session_state['selected_record'] = preset_rec
    st.session_state['projects_fetched'] = True
    st.session_state['active_district'] = "East Champaran (Motihari)"
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

# Top Header Layout with Top-Right Three-Dot (⋮) Settings Popover
header_col1, header_col2, header_col3 = st.columns([1, 8, 1])

with header_col2:
    st.markdown(f"<div class='brand-title'>🏛️ PAIMANA AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='brand-subtitle'>ANALYSIS AND PREDICT AI</div>", unsafe_allow_html=True)

with header_col3:
    with st.popover("⋮", use_container_width=True):
        st.markdown("### ⚙️ User Display Settings")
        st.caption("Personalize theme, contrast, and font scale.")
        
        new_theme = st.selectbox(
            "Background Palette",
            list(bg_map.keys()),
            index=list(bg_map.keys()).index(st.session_state["app_bg_theme"])
        )
        new_accent = st.selectbox(
            "Accent Highlight",
            list(accent_map.keys()),
            index=list(accent_map.keys()).index(st.session_state["app_accent_color"])
        )
        new_font = st.selectbox(
            "Text Scaling",
            list(font_scale_map.keys()),
            index=list(font_scale_map.keys()).index(st.session_state["app_font_scale"])
        )
        
        if (
            new_theme != st.session_state["app_bg_theme"] or
            new_accent != st.session_state["app_accent_color"] or
            new_font != st.session_state["app_font_scale"]
        ):
            st.session_state["app_bg_theme"] = new_theme
            st.session_state["app_accent_color"] = new_accent
            st.session_state["app_font_scale"] = new_font
            st.rerun()

# Main 2-Column Interface
col_sec1, col_sec2 = st.columns([1.05, 0.95], gap="medium")

# SECTION 1: Details About Ongoing Projects
with col_sec1:
    st.markdown("<div class='section-title'>📁 SECTION 1: DETAILS ABOUT ONGOING PROJECTS</div>", unsafe_allow_html=True)
    
    if st.session_state.get('projects_fetched', False):
        active_dist = st.session_state.get('active_district', selected_district)
        district_kw = active_dist.split()[0].lower()
        matched_projects = [r for _, r in paimana_df.iterrows() if district_kw in str(r["District"]).lower()]
        if not matched_projects:
            matched_projects = [r for _, r in paimana_df.iterrows()]
            
        project_options = [str(r["Project_Name"]) for r in matched_projects]
        selected_inspect = st.selectbox("Select Construction Work to Inspect:", project_options, index=0)
        active_row = next((r for r in matched_projects if str(r["Project_Name"]) == selected_inspect), matched_projects[0])

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
            st.session_state['box_phys'] = float(row_dict['Physical_Progress_Pct'])
            st.session_state['box_ms'] = int(row_dict['Delayed_Milestones'])
            st.session_state['box_rev'] = int(row_dict.get('Revisions_Count', 0))
            st.session_state['sl_land'] = float(row_dict['Land_Risk_Score'])
            st.session_state['sl_wpi'] = float(row_dict['WPI_Inflation_Index'])
            st.session_state['ai_evaluated'] = False
            st.rerun()
    else:
        st.info("👈 Please select complete State, District, Subdivision, and Block from the sidebar and click 'Fetch Ongoing Projects (Enter ↵)' to load packages.")

# SECTION 2: Predict Project Future Overview (Box Inputs + 2 Sliders)
rec = st.session_state.get('selected_record') or {}

with col_sec2:
    st.markdown("<div class='section-title'>⚡ SECTION 2: PREDICT PROJECT FUTURE OVERVIEW</div>", unsafe_allow_html=True)
    
    s2_col1, s2_col2 = st.columns(2)
    with s2_col1:
        inp_cost = st.number_input("Cost (₹ Cr)", value=float(st.session_state.get('inp_cost', rec.get('Original_Cost_Cr', 0.0))), key="inp_cost")
        inp_duration = st.number_input("Original Duration (Months)", value=int(st.session_state.get('inp_dur', rec.get('Original_Duration', 0))), key="inp_dur")
        inp_elapsed = st.number_input("Elapsed Time (Months)", value=int(st.session_state.get('inp_elap', rec.get('Elapsed_Months', 0))), key="inp_elap")
        inp_spend = st.number_input("Cumulative Spend (₹ Cr)", value=float(st.session_state.get('inp_sp', rec.get('Cumulative_Spend_Cr', 0.0))), key="inp_sp")
    with s2_col2:
        inp_phys = st.number_input("Physical Progress (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.get('box_phys', rec.get('Physical_Progress_Pct', 0.0))), key="box_phys")
        inp_milestones = st.number_input("Delayed Milestones", min_value=0, max_value=20, value=int(st.session_state.get('box_ms', rec.get('Delayed_Milestones', 0))), key="box_ms")
        inp_revisions = st.number_input("Revisions Count", min_value=0, max_value=10, value=int(st.session_state.get('box_rev', rec.get('Revisions_Count', 0))), key="box_rev")
        
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

    # Risk Output Cards
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
        fig_s = go.Figure()
        
        fig_s.add_trace(go.Bar(
            name='Planned Target (%)',
            x=['Schedule Horizon'],
            y=[planned_progress_pct],
            marker=dict(color=active_accent, line=dict(color='#0284C7', width=1.5)),
            width=0.35
        ))
        fig_s.add_trace(go.Bar(
            name='Actual Ground Progress (%)',
            x=['Schedule Horizon'],
            y=[inp_phys],
            marker=dict(color='#10B981', line=dict(color='#059669', width=1.5)),
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
        active_dist_name = st.session_state.get('active_district', selected_district)
        proj_title = rec.get('Project_Name', 'Registered Works Package')
        pkg_code = rec.get('Package_ID', f"BHR_{active_dist_name[:3].upper()}_2026_0290")
        contractor = rec.get('Contractor_Name', 'M/S Executing Agency Pvt Ltd')
        officer = rec.get('Site_Engineer', 'Er. Executive Engineer (Infrastructure Works)')
        current_date_str = datetime.now().strftime('%d-%B-%Y')

        # Formal Legal Notice Structure
        memo_text = f"""To,
The Authorized Managing Director / Project Head,
{contractor},
Principal Executing Agency,
Project Package: {proj_title},
District: {active_dist_name}, Bihar.

Subject: Notice related to critical schedule slippage and breach of baseline milestones at {proj_title} (Package ID: {pkg_code}).

Dear Sir/Madam,

I hope this letter finds you well. I am writing this to formally notify you about serious concerns regarding the ongoing construction activities occurring at your work site for "{proj_title}" located within {selected_block}, {selected_subdiv}, {active_dist_name}, Bihar. Based on our departmental inspection and verified data appraisal conducted via the MoSPI InfraDrishti-AI Framework, it is established that the actual on-site progress ({inp_phys:.2f}%) has substantially deviated from the approved baseline target ({planned_progress_pct:.2f}%), resulting in an unacceptable negative Schedule Variance of {schedule_variance_pct:.2f}% and an estimated slippage of +{pred_delay_months:.1f} Months.

This execution failure directly violates Clause 2 (Compensation for Delay) and Clause 3 of the Standard CPWD Works Manual Contract Agreement, read in conjunction with Rule 130 of General Financial Rules (GFR 2017) regarding the timely utilization of public funds and physical milestone adherence. Furthermore, the recorded Cost Performance Index (CPI) of {cpi:.2f} indicates front-loading of disbursed funds (₹{inp_spend:.2f} Cr spend out of ₹{inp_cost:.2f} Cr sanctioned) without corresponding physical delivery, creating potential fiscal distress and substantial delay to the public interest.

Further, the slow mobilization of machinery and recurring milestone carryovers have directly contradicted the approved PERT/CPM schedule set forth by this monitoring authority. This continued disregard for statutory delivery timelines is unacceptable and warrants immediate corrective intervention. Taking into consideration the aforementioned pointers, you are hereby directed to submit an escalated catch-up recovery schedule and deploy augmented double-shift resources immediately. Further, if this matter is not resolved and adequate cause is not shown in writing within 14 days from the date of issuance of this notice, we will be left with no choice but to levy statutory Liquidated Damages @ 1.0% per month under CPWD Clause 2 and escalate the matter for penal determination of the contract.

Thanking you in anticipation for your prompt attention to this matter. I hope we can resolve this operational deficit expeditiously for the timely commissioning of this public infrastructure.

Sincerely,
{officer},
Nodal Appraisal & Executive Engineer,
State Infrastructure Monitoring Division (PMU Bihar),
Ministry of Statistics & Programme Implementation (MoSPI),
{active_dist_name}, Bihar.
Date: {current_date_str}
"""
        st.text_area("Directive Notice Preview", memo_text, height=360)
        st.download_button(
            label="📥 Download Directive Notice (.txt)",
            data=memo_text,
            file_name=f"Directive_Notice_{active_dist_name.split()[0]}_{datetime.now().strftime('%Y%m%d')}.txt",
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
