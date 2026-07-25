import streamlit as st
import pandas as pd
import joblib

# ---------- Page config ----------
st.set_page_config(page_title="AutoValue — Car Price Estimator",
                   page_icon="🚗", layout="wide")

# ---------- Load model & encoders ----------
model = joblib.load('car_price_model.pkl')
brand_encoder = joblib.load('brand_encoder.pkl')
model_encoder = joblib.load('model_encoder.pkl')
columns = joblib.load('model_columns.pkl')

# ---------- Global CSS ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    /* Hide streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}

    .stApp {
        background: #0a0e1a;
        font-family: 'Inter', sans-serif;
    }

    .block-container {padding-top: 1rem; max-width: 1100px;}

    /* ---- Hero ---- */
    .hero {
        position: relative;
        background:
            linear-gradient(135deg, rgba(10,14,26,0.85) 0%, rgba(10,14,26,0.55) 100%),
            url('https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        padding: 55px 45px;
        margin-bottom: 28px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .hero-badge {
        display: inline-block;
        background: rgba(99,102,241,0.15);
        color: #a5b4fc;
        border: 1px solid rgba(99,102,241,0.35);
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 18px;
    }
    .hero h1 {
        font-family: 'Poppins', sans-serif;
        color: #ffffff;
        font-size: 46px;
        font-weight: 800;
        line-height: 1.1;
        margin: 0 0 12px 0;
    }
    .hero h1 span { color: #818cf8; }
    .hero p {
        color: #cbd5e1;
        font-size: 17px;
        max-width: 520px;
        margin: 0;
        line-height: 1.6;
    }

    /* ---- Section card ---- */
    .card {
        background: #131a2e;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 28px 32px;
        margin-bottom: 22px;
    }
    .card-title {
        font-family: 'Poppins', sans-serif;
        color: #ffffff;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .card-sub {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 22px;
    }

    /* ---- Input labels ---- */
    .stSelectbox label, .stNumberInput label {
        color: #94a3b8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    /* Input fields */
    .stSelectbox div[data-baseweb="select"] > div,
    .stNumberInput div[data-baseweb="input"] > div {
        background: #0a0e1a !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    .stNumberInput input { color: #ffffff !important; }

    /* ---- Predict button ---- */
    div.stButton {
        margin-top: 10px;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 17px !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 0 !important;
        width: 100% !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        box-shadow: 0 6px 20px rgba(99,102,241,0.3) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 28px rgba(99,102,241,0.45) !important;
        color: #ffffff !important;
    }
    div.stButton > button:active,
    div.stButton > button:focus,
    div.stButton > button:focus:not(:active) {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 6px 20px rgba(99,102,241,0.35) !important;
        outline: none !important;
    }

    /* ---- Result ---- */
    .result {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        border-radius: 18px;
        padding: 38px;
        text-align: center;
        margin-top: 8px;
        box-shadow: 0 15px 40px rgba(16,185,129,0.3);
    }
    .result .label {
        color: rgba(255,255,255,0.85);
        font-size: 15px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .result .price {
        font-family: 'Poppins', sans-serif;
        color: #ffffff;
        font-size: 52px;
        font-weight: 800;
        margin: 0;
        line-height: 1;
    }
    .result .note {
        color: rgba(255,255,255,0.8);
        font-size: 13px;
        margin-top: 14px;
    }

    /* Feature chips under hero */
    .chips { display: flex; gap: 14px; margin-top: 26px; flex-wrap: wrap; }
    .chip {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 14px 20px;
        flex: 1;
        min-width: 140px;
    }
    .chip .num {
        font-family: 'Poppins', sans-serif;
        color: #818cf8;
        font-size: 22px;
        font-weight: 700;
    }
    .chip .txt { color: #94a3b8; font-size: 13px; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ AI-POWERED VALUATION</div>
    <h1>Know your car's<br><span>true market value</span></h1>
    <p>Enter your vehicle details and our machine learning model
       instantly estimates a fair selling price based on thousands of real listings.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Input card ----------
st.markdown('<div class="card"><div class="card-title">Vehicle Details</div>'
            '<div class="card-sub">Fill in the details below for an accurate estimate</div>',
            unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    brand = st.selectbox("Brand", list(brand_encoder.classes_))
    fuel = st.selectbox("Fuel Type", ['Diesel', 'Petrol', 'LPG', 'CNG'])
    car_age = st.number_input("Car Age (years)", 0, 30, 5)
    engine = st.number_input("Engine (CC)", 600, 3500, 1200)

with c2:
    car_model = st.selectbox("Model", list(model_encoder.classes_))
    transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])
    km_driven = st.number_input("Kilometers Driven", 0, 400000, 50000)
    max_power = st.number_input("Max Power (bhp)", 30.0, 400.0, 80.0)

with c3:
    seller_type = st.selectbox("Seller Type", ['Individual', 'Dealer', 'Trustmark Dealer'])
    owner = st.selectbox("Owner", ['First Owner', 'Second Owner', 'Third Owner',
                                   'Fourth & Above Owner', 'Test Drive Car'])
    mileage = st.number_input("Mileage (km/l)", 0.0, 50.0, 20.0)
    seats = st.number_input("Seats", 2, 10, 5)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Predict ----------
predict = st.button("Estimate Price  →", use_container_width=True)

if predict:
    fuel_num = {'Diesel': 0, 'Petrol': 1, 'LPG': 2, 'CNG': 3}[fuel]
    seller_num = {'Individual': 0, 'Dealer': 1, 'Trustmark Dealer': 2}[seller_type]
    transmission_num = {'Manual': 0, 'Automatic': 1}[transmission]
    owner_num = {'First Owner': 1, 'Second Owner': 2, 'Third Owner': 3,
                 'Fourth & Above Owner': 4, 'Test Drive Car': 0}[owner]

    brand_num = brand_encoder.transform([brand])[0]
    model_num = model_encoder.transform([car_model])[0]

    new_car = pd.DataFrame([{
        'km_driven': km_driven, 'fuel': fuel_num, 'seller_type': seller_num,
        'transmission': transmission_num, 'owner': owner_num, 'mileage': mileage,
        'engine': engine, 'max_power': max_power, 'seats': seats,
        'car_age': car_age, 'brand': brand_num, 'model': model_num
    }])
    new_car = new_car[columns]

    price = model.predict(new_car)[0]

    st.markdown(f"""
    <div class="result">
        <div class="label">Estimated Selling Price</div>
        <div class="price">₹ {format(round(price), ",")}</div>
        <div class="note">Based on machine learning analysis · Actual price may vary</div>
    </div>
    """, unsafe_allow_html=True)