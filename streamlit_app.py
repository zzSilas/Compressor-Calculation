import streamlit as st

st.title("🎈 Compressor COP calculation")
compressor_name = st.text_input("Compressor Name")
T_evap = st.number_input("Evaporating Temperature (°C)", value=0.0)
T_cond = st.number_input("Condensing Temperature (°C)", value=0.0)
tSuc = st.number_input("Suction Temperature (°C)", value=0.0)
nCompressor = st.number_input("Compressor Efficiency (%)", value=100.0)
