import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import io

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="Climate Prediction Dashboard", layout="wide")

# ২. আপনার দেওয়া ডেটা (মডেল ট্রেনিং এর জন্য)
csv_data = """rainfall,population_density,elevation,temperature,flood_risk
200,1200,5,30,High
150,900,10,29,Medium
100,700,20,28,Low
220,1300,4,31,High
180,1100,6,30,High
140,850,12,29,Medium
90,600,25,27,Low
210,1250,5,30,High
160,950,8,29,Medium
110,750,18,28,Low"""

df = pd.read_csv(io.StringIO(csv_data))

# ৩. মেশিন লার্নিং মডেল প্রিপারেশন
# LabelEncoder দিয়ে 'High', 'Medium', 'Low' কে সংখ্যায় (0, 1, 2) রূপান্তর
le = LabelEncoder()
df['risk_encoded'] = le.fit_transform(df['flood_risk'])

# ফিচার (X) এবং টার্গেট (y) আলাদা করা
X = df[['rainfall', 'population_density', 'elevation', 'temperature']]
y = df['risk_encoded']

# Random Forest মডেল ট্রেনিং
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ৪. ড্যাশবোর্ড UI
st.title("🌊 Climate Risk Prediction & Mapping Dashboard")
st.markdown("এই ড্যাশবোর্ডটি মেশিন লার্নিং ব্যবহার করে বন্যার ঝুঁকি প্রেডিক্ট করে।")

# ৫. সাইডবার ইনপুট (ইউজার ভ্যালু দিয়ে চেক করতে পারবে)
st.sidebar.header("🔍 Input Parameters for Prediction")
rain = st.sidebar.slider("Rainfall (mm)", 50, 300, 150)
pop = st.sidebar.number_input("Population Density", 500, 2000, 1000)
elev = st.sidebar.slider("Elevation (m)", 0, 50, 10)
temp = st.sidebar.slider("Temperature (°C)", 20, 40, 30)

# ৬. প্রেডিকশন লজিক
input_data = [[rain, pop, elev, temp]]
prediction_encoded = model.predict(input_data)
prediction_label = le.inverse_transform(prediction_encoded)[0]

# ৭. ড্যাশবোর্ড মেইন সেকশন
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("🎯 Prediction Result")
    # কালার কোডিং
    bg_color = "#ff4d4d" if prediction_label == "High" else "#ffa502" if prediction_label == "Medium" else "#2ed573"
    
    st.markdown(f"""
        <div style="background-color:{bg_color}; padding:20px; border-radius:10px; text-align:center;">
            <h2 style="color:white; margin:0;">Flood Risk: {prediction_label}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📋 Dataset Used for Training")
    st.dataframe(df[['rainfall', 'population_density', 'elevation', 'temperature', 'flood_risk']])

with col2:
    st.subheader("📈 Risk Factors Analysis")
    # ফিচারের গুরুত্ব বা ইমপোর্টেন্স দেখা
    feature_imp = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_})
    st.bar_chart(feature_imp.set_index('Feature'))
    st.caption("মডেলের কাছে কোন ফ্যাক্টরটি বেশি গুরুত্বপূর্ণ তা উপরের চার্টে দেখা যাচ্ছে।")

# ৮. রিয়েল ম্যাপের সাথে কানেকশন (ঐচ্ছিক)
st.divider()
st.info("💡 টিপস: বাম পাশের স্লাইডারগুলো পরিবর্তন করে দেখুন কীভাবে বন্যার ঝুঁকি পরিবর্তিত হয়।")
