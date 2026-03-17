import pandas as pd
import folium
import io

# ১. ডাটা লোড
csv_data = """location,lat,lon,rainfall,population_density,elevation,temperature,flood_risk
Sunamganj,25.0715,91.3992,200,1200,5,30,High
Kurigram,25.8072,89.6295,150,900,10,29,Medium
Panchagarh,26.3333,88.5584,100,700,20,28,Low
Sirajganj,24.4534,89.7042,220,1300,4,31,High
Netrokona,24.8700,90.7300,180,1100,6,30,High
Gaibandha,25.3297,89.5430,140,850,12,29,Medium
Kushtia,23.9013,89.1200,90,600,25,27,Low
Bhola,22.6859,90.6455,210,1250,5,30,High
Bagerhat,22.6515,89.7859,160,950,8,29,Medium
Chuadanga,23.6401,88.8500,110,750,18,28,Low"""

df = pd.read_csv(io.StringIO(csv_data))

# ২. ম্যাপ সেটআপ (বাংলাদেশ সেন্টার)
m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles='CartoDB positron')

# ৩. ম্যাপে ডাইনামিক সার্কেল মার্কার যোগ করা
for index, row in df.iterrows():
    risk = row['flood_risk']
    
    # রিস্ক লেভেল অনুযায়ী রঙ নির্ধারণ
    color = '#d63031' if risk == 'High' else '#fd9644' if risk == 'Medium' else '#20bf6b'
    
    popup_info = f"""
    <div style="font-family: Arial; width: 180px;">
        <h4 style="margin:0 0 5px 0;">{row['location']}</h4>
        <b>Flood Risk:</b> <span style="color:{color}">{risk}</span><br>
        <b>Rainfall:</b> {row['rainfall']} mm<br>
        <b>Elevation:</b> {row['elevation']} m<br>
        <b>Population Density:</b> {row['population_density']}
    </div>
    """
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['rainfall'] / 15,  # বৃষ্টিপাত অনুযায়ী সার্কেল সাইজ
        popup=folium.Popup(popup_info, max_width=250),
        tooltip=f"{row['location']} ({risk} Risk)",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        weight=1.5
    ).add_to(m)

# ৪. ম্যাপ সেভ করা
m.save("climate_risk_map.html")
print("ম্যাপ তৈরি হয়েছে! 'climate_risk_map.html' ফাইলটি ব্রাউজারে ওপেন করুন।")
m
