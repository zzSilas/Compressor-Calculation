import streamlit as st

st.title("🎈 Compressor COP calculation")
# 输入
compressor_name = st.text_input("Compressor Name")
T_evap = st.number_input("Evaporating Temperature (°C)", value=0.0)
T_cond = st.number_input("Condensing Temperature (°C)", value=0.0)
tSuc = st.number_input("Suction Temperature (°C)", value=0.0)
nCompressor = st.number_input("Compressor Efficiency (%)", value=100.0)
# 上传Excel文件
uploaded_file = st.file_uploader("Upload Messdata.xlsx", type=["xlsx"])
if uploaded_file is not None:
    Messdata = pd.read_excel(uploaded_file)
    st.write(data)
if st.button("Calculate COP"):
    # 这里放置你的计算逻辑
    # 例如:
    COP = (T_cond - T_evap) / (T_cond - tSuc) * (nCompressor / 100)
    
    st.success(f"The calculated COP for {compressor_name} is: {COP:.2f}")
