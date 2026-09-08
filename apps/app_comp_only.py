import joblib
import streamlit as st
import pandas as pd

model = joblib.load('models/comp_only_model.joblib')

st.markdown("""
    <style>
    h1 {
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Valorant Composition Win Predictor")
st.caption("⚠️ This model achieved only ~52% accuracy in testing — barely above random guessing. Predictions here are illustrative, not confident forecasts of match outcomes.")

controller = st.slider('Controller', min_value=0, max_value=5, value=0)
duelist = st.slider('Duelist', min_value=0, max_value=5, value=0)
initiator = st.slider('Initiator', min_value=0, max_value=5, value=0)
sentinel = st.slider('Sentinel', min_value=0, max_value=5, value=0)



submitted = st.button("Predict")

if submitted:
    total = controller + duelist + initiator + sentinel
    if total != 5:
        st.error(f"Team composition must total 5 players (currently {total}).")
    else:
        input_data = pd.DataFrame([[controller, duelist, initiator, sentinel]],
                                    columns=['Controller', 'Duelist', 'Initiator', 'Sentinel'])
        probability = model.predict_proba(input_data)
        win_prob = probability[0][1]
        st.metric("Predicted Win Probability", f"{win_prob:.0%}")