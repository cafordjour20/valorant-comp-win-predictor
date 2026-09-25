import joblib
import streamlit as st
import pandas as pd

model = joblib.load('models/comp_map_model.joblib')

st.markdown("""
    <style>
    h1 {
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Valorant Composition Win Predictor")
st.caption("⚠️ This model which factors comp and map achieved only ~52% accuracy in testing — barely above random guessing. Predictions here are illustrative, not confident forecasts of match outcomes.")

input_dict = {feature: 0 for feature in model.feature_names_in_}

input_dict['Controller'] = st.slider('Controller', min_value=0, max_value=5, value=0)
input_dict['Duelist'] = st.slider('Duelist', min_value=0, max_value=5, value=0)
input_dict['Initiator'] = st.slider('Initiator', min_value=0, max_value=5, value=0)
input_dict['Sentinel'] = st.slider('Sentinel', min_value=0, max_value=5, value=0)

model_map_names = model.feature_names_in_
maps = [map_name.replace('map_name_', '') for map_name in model_map_names if map_name.startswith('map_name_')]

selected_map = st.selectbox(label="Map", options=maps)

map_key = f"map_name_{selected_map}"
if map_key in input_dict:
    input_dict[map_key] = 1

submitted = st.button("Predict")

if submitted:
    total = input_dict['Controller'] + input_dict['Duelist'] + input_dict['Initiator'] + input_dict['Sentinel']
    if total != 5:
        st.error(f"Team composition must total 5 players (currently {total}).")
    else:
        input_data = pd.DataFrame([input_dict])
        probability = model.predict_proba(input_data)
        win_prob = probability[0][1]
        st.metric("Predicted Win Probability", f"{win_prob:.0%}")