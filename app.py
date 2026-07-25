import streamlit as st
import pandas as pd
import joblib

# Load model and encoders
model = joblib.load('car_price_model.pkl')
brand_encoder = joblib.load('brand_encoder.pkl')
model_encoder = joblib.load('model_encoder.pkl')
columns = joblib.load('model_columns.pkl')

st.title("Car Price Prediction")
st.write("Enter the car details below to estimate its selling price.")

# Inputs
brand = st.selectbox("Brand", list(brand_encoder.classes_))

car_model = st.selectbox("Model", list(model_encoder.classes_))

car_age = st.number_input("Car Age (years)", min_value=0, max_value=30, value=5)

km_driven = st.number_input("Kilometers Driven", min_value=0, max_value=400000, value=50000)

fuel = st.selectbox("Fuel Type", ['Diesel', 'Petrol', 'LPG', 'CNG'])

seller_type = st.selectbox("Seller Type", ['Individual', 'Dealer', 'Trustmark Dealer'])

transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])

owner = st.selectbox("Owner", ['First Owner', 'Second Owner', 'Third Owner',
                               'Fourth & Above Owner', 'Test Drive Car'])

mileage = st.number_input("Mileage (km/l)", min_value=0.0, max_value=50.0, value=20.0)

engine = st.number_input("Engine (CC)", min_value=600, max_value=3500, value=1200)

max_power = st.number_input("Max Power (bhp)", min_value=30.0, max_value=400.0, value=80.0)

seats = st.number_input("Seats", min_value=2, max_value=10, value=5)

# Predict
if st.button("Predict Price"):

    # Convert text to numbers (same mapping used during training)
    fuel_num = {'Diesel': 0, 'Petrol': 1, 'LPG': 2, 'CNG': 3}[fuel]
    seller_num = {'Individual': 0, 'Dealer': 1, 'Trustmark Dealer': 2}[seller_type]
    transmission_num = {'Manual': 0, 'Automatic': 1}[transmission]
    owner_num = {'First Owner': 1, 'Second Owner': 2, 'Third Owner': 3,
                 'Fourth & Above Owner': 4, 'Test Drive Car': 0}[owner]

    # Use the SAME encoders from training
    brand_num = brand_encoder.transform([brand])[0]
    model_num = model_encoder.transform([car_model])[0]

    # Build one row in the correct column order
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

    price = model.predict(new_car)[0]

    st.success("Predicted Price: INR " + format(round(price), ","))
    st.caption("This is an estimated price. Actual price may vary.")