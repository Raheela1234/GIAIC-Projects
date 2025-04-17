import streamlit as st

# Apply Custom CSS for Background
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #95afc0;
}
[data-testid="stSidebar"] {
    background-color: #dff9fb;
}
h1 {
    color: #ff6f00;
    text-align: center;
}
.stButton button {
    background-color: #6ab04c;
    color: white;
    border-radius: 10px;
    padding: 10px;
    width: 100%;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Title
st.title("🔄 Multi-Unit Converter")

# Sidebar Navigation
st.sidebar.title("⚡ Quick Navigation")
category = st.sidebar.radio("Choose a Category:", ["Length", "Weight", "Temperature"])

# Conversion Dictionaries
length_conversion = {
    "Kilometers to Miles": 0.621371,
    "Miles to Kilometers": 1.60934,
    "Meters to Feet": 3.28084,
    "Feet to Meters": 0.3048
}

weight_conversion = {
    "Kilograms to Pounds": 2.20462,
    "Pounds to Kilograms": 0.453592
}

temperature_conversion = {
    "Celsius to Fahrenheit": lambda c: (c * 9/5) + 32,
    "Fahrenheit to Celsius": lambda f: (f - 32) * 5/9
}

# Category Selection
st.subheader(f"🛠 Convert {category} Units")

if category == "Length":
    conversion_type = st.selectbox("📏 Select conversion:", list(length_conversion.keys()))
    value = st.slider("Enter value:", min_value=0.0, max_value=1000.0, step=0.1)
    if st.button("Convert"):
        result = value * length_conversion[conversion_type]
        st.success(f"✅ Converted Value: {result:.2f}")

elif category == "Weight":
    conversion_type = st.selectbox("⚖️ Select conversion:", list(weight_conversion.keys()))
    value = st.slider("Enter value:", min_value=0.0, max_value=1000.0, step=0.1)
    if st.button("Convert"):
        result = value * weight_conversion[conversion_type]
        st.success(f"✅ Converted Value: {result:.2f}")

elif category == "Temperature":
    conversion_type = st.selectbox("🌡️ Select conversion:", list(temperature_conversion.keys()))
    value = st.slider("Enter value:", min_value=-100.0, max_value=100.0, step=0.1)
    if st.button("Convert"):
        result = temperature_conversion[conversion_type](value)
        st.success(f"✅ Converted Value: {result:.2f}")