import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide",
)

# ---------------- CSS ---------------- #
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#111827);
    color:white;
}

.main-title{
    text-align:center;
    font-size:48px;
    font-weight:700;
    color:white;
    margin-bottom:0;
}

.sub-title{
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
    margin-bottom:35px;
}

.card{
    background:rgba(255,255,255,.08);
    backdrop-filter: blur(15px);
    padding:30px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,.15);
    box-shadow:0 10px 30px rgba(0,0,0,.3);
}

.result-card{
    background:linear-gradient(135deg,#10b981,#059669);
    padding:25px;
    border-radius:18px;
    text-align:center;
    margin-top:25px;
}

.price{
    font-size:45px;
    font-weight:bold;
    color:white;
}

.small{
    color:#e5e7eb;
}

div.stButton > button{
    width:100%;
    height:55px;
    border-radius:12px;
    border:none;
    background:linear-gradient(90deg,#2563eb,#3b82f6);
    color:white;
    font-size:18px;
    font-weight:bold;
}

div.stButton > button:hover{
    background:linear-gradient(90deg,#1d4ed8,#2563eb);
    transform:scale(1.02);
}

[data-testid="stMetricValue"]{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Load Model ---------------- #

model = joblib.load("car_price_model.pkl")
brand_encoder = joblib.load("brand_encoder.pkl")
model_encoder = joblib.load("model_encoder.pkl")
columns = joblib.load("model_columns.pkl")

# ---------------- Header ---------------- #

st.markdown("<h1 class='main-title'>🚗 Car Price Predictor</h1>", unsafe_allow_html=True)

st.markdown(
"<p class='sub-title'>Predict the estimated resale value of your vehicle using Machine Learning.</p>",
unsafe_allow_html=True
)

st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    brand = st.selectbox(
        "Brand",
        list(brand_encoder.classes_)
    )

    car_model = st.selectbox(
        "Model",
        list(model_encoder.classes_)
    )

    car_age = st.slider(
        "Car Age",
        0,
        30,
        5
    )

    km_driven = st.number_input(
        "Kilometers Driven",
        0,
        400000,
        50000
    )

    fuel = st.selectbox(
        "Fuel Type",
        ['Diesel','Petrol','LPG','CNG']
    )

    seller_type = st.selectbox(
        "Seller Type",
        ['Individual','Dealer','Trustmark Dealer']
    )

with col2:

    transmission = st.selectbox(
        "Transmission",
        ['Manual','Automatic']
    )

    owner = st.selectbox(
        "Owner",
        ['First Owner',
         'Second Owner',
         'Third Owner',
         'Fourth & Above Owner',
         'Test Drive Car']
    )

    mileage = st.number_input(
        "Mileage (km/l)",
        0.0,
        50.0,
        20.0
    )

    engine = st.number_input(
        "Engine (CC)",
        600,
        3500,
        1200
    )

    max_power = st.number_input(
        "Max Power (bhp)",
        30.0,
        400.0,
        80.0
    )

    seats = st.slider(
        "Seats",
        2,
        10,
        5
    )

predict = st.button("Predict Car Price")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Prediction ---------------- #

if predict:

    fuel_num = {'Diesel':0,'Petrol':1,'LPG':2,'CNG':3}[fuel]

    seller_num = {
        'Individual':0,
        'Dealer':1,
        'Trustmark Dealer':2
    }[seller_type]

    transmission_num = {
        'Manual':0,
        'Automatic':1
    }[transmission]

    owner_num = {
        'First Owner':1,
        'Second Owner':2,
        'Third Owner':3,
        'Fourth & Above Owner':4,
        'Test Drive Car':0
    }[owner]

    brand_num = brand_encoder.transform([brand])[0]
    model_num = model_encoder.transform([car_model])[0]

    new_car = pd.DataFrame([{

        'km_driven': km_driven,
        'fuel': fuel_num,
        'seller_type': seller_num,
        'transmission': transmission_num,
        'owner': owner_num,
        'mileage': mileage,
        'engine': engine,
        'max_power': max_power,
        'seats': seats,
        'car_age': car_age,
        'brand': brand_num,
        'model': model_num

    }])

    new_car = new_car[columns]

    prediction = model.predict(new_car)[0]

    st.markdown(f"""
    <div class="result-card">
        <h2>Estimated Selling Price</h2>
        <div class="price">₹ {prediction:,.0f}</div>
        <p class="small">
        This value is generated using a Machine Learning model and should be considered an estimate.
        </p>
    </div>
    """, unsafe_allow_html=True)