from flask import Flask, render_template, request
import sqlite3
import joblib
import pandas as pd
import os

app = Flask(__name__)

# ---------------- ML Models ----------------
soil_model = joblib.load("soil_model.pkl")
crop_model = joblib.load("crop_model.pkl")

# ---------------- Dataset ----------------
rotation_path = os.path.join("dataset", "crop_rotation.csv")
rotation_data = pd.read_csv(rotation_path)

# ---------------- Language ----------------
texts = {
    "en": {
        "title": "🌱 Soil Analyzer System",
        "ph": "pH Value",
        "moisture": "Moisture",
        "n": "Nitrogen",
        "p": "Phosphorus",
        "k": "Potassium",
        "analyze": "Analyze",
        "voice": "Voice Input",
        "history": "History",
        "follow":"Follow crop rotation",
        "result": "Result",
        "note_title": "Important Note",
"note1": "pH – Soil acidity or alkalinity.",
"note2": "Nitrogen – Helps leaf growth.",
"note3": "Phosphorus – Root and flower growth.",
"note4": "Potassium – Disease resistance.",
 "fertile": "Fertile",
        "moderate": "Moderate",
        "poor": "Poor",
        "low": "Low",
        "high": "High",
        "follow": "Follow crop rotation.",       
"soil": "Soil",
"crop": "Crop",
"rotation": "Crop Rotation Advice",
"avoid": "Avoid growing",
"for": "for next",
"months": "months",
"grow": "Grow",
"restore": "to restore soil",
"back": "Back",
"nutrient": "Nutrient Level",
"fertilizer_title": "Fertilizer Advice",
# -------- Location Soil Data --------

    "Thanjavur": {
        "soil": "Alluvial Soil",
        "category": "Fertile",
        "uses": "Rice, Sugarcane, Banana"
    },
    "Theni": {
        "soil": "Red Soil",
        "category": "Fertile",
        "uses": "Cotton, Maize"
    },
    "Coimbatore": {
        "soil": "Red Soil",
        "category": "Moderate",
        "uses": "Cotton, Groundnut"
    },
    "Gobi": {
        "soil": "Clay Soil",
        "category": "Moderate",
        "uses": "Turmeric, Sugarcane"
    },
    "Tiruchendur": {
        "soil": "Sandy Soil",
        "category": "Coastal",
        "uses": "Coconut, Cashew"
    }


       
    },

    "ta": {
        "title": "🌱 மண் ஆய்வு முறை",
        "ph": "pH மதிப்பு",
        "moisture": "ஈரப்பதம்",
        "n": "நைட்ரஜன்",
        "p": "பாஸ்பரஸ்",
        "k": "பொட்டாசியம்",
        "analyze": "பரிசோதனை செய்",
        "voice": "குரல் உள்ளீடு",
        "result": "முடிவு",
        "history":"வரலாறு",
        "follow": "பயிர் மாற்றத்தை பின்பற்றவும்",
        "note_title":"முக்கிய குறிப்பு",
"note1": "pH – மண்ணின் அமில அல்லது கார தன்மை.",
"note2": "நைட்ரஜன் – இலை வளர்ச்சிக்கு உதவும்.",
"note3": "பாஸ்பரஸ் – வேர் மற்றும் மலர் வளர்ச்சி.",
"note4": "பொட்டாசியம் – நோய் எதிர்ப்பு.",
"soil": "மண் நிலை",
"crop": "பயிர்",
"rotation": "பயிர் மாற்ற ஆலோசனை",
"avoid": "அடுத்த",
"for": "",
"months": "மாதங்கள் இந்த பயிரை தவிர்க்கவும்",
"grow": "வளர்க்க",
"restore": "மண் சீரமைக்க",
"back": "மீண்டும்",
 "fertile": "சத்து மண்",
 "nutrient": "ஊட்டச்சத்து நிலை",
"fertilizer_title": "உர பரிந்துரை",
        "moderate": "மிதமான மண்",
        "poor": "பலவீனமான மண்",
        "low": "குறைவு",
        "high": "அதிகம்",
        "follow": "பயிர் முறை மாற்றத்தை பின்பற்றவும்.",
"தஞ்சாவூர்": {
        "soil": "ஆலுவியல் மண்",
        "category": "உரமுள்ள மண்",
        "uses": "நெல், கரும்பு, வாழை"
    },
    "தேனி": {
        "soil": "செம்மண்",
        "category": "உரமுள்ள மண்",
        "uses": "பருத்தி, மக்காச்சோளம்"
    },
    "கோயம்புத்தூர்": {
        "soil": "செம்மண்",
        "category": "மிதமான மண்",
        "uses": "பருத்தி, நிலக்கடலை"
    },
    "கோபி": {
        "soil": "களிமண்",
        "category": "மிதமான மண்",
        "uses": "மஞ்சள், கரும்பு"
    },
    "திருச்செந்தூர்": {
        "soil": "மணல் மண்",
        "category": "கடற்கரை மண்",
        "uses": "தேங்காய், முந்திரி"
    }
    }
}

# ---------------- Database ----------------
def init_db():
    conn = sqlite3.connect("soil.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS soil(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ph REAL,
        moisture REAL,
        n REAL,
        p REAL,
        k REAL,
        soil TEXT,
        crop TEXT
    )
    """)
    conn.close()

init_db()


# ---------------- HOME ----------------
@app.route("/")
def home():
    lang = request.args.get("lang", "en")
    return render_template("index.html", t=texts[lang], lang=lang)


# ---------------- ANALYZE ----------------
@app.route("/analyze", methods=["POST"])
def analyze():
    lang = request.args.get("lang", "en")
    t = texts[lang]
    ph = float(request.form.get("ph" ) or 0)
    moisture = float(request.form.get("moisture",) or 0) 
    n = float(request.form.get("n") or 0) 
    p = float(request.form.get("p",) or 0)
    k = float(request.form.get("k",) or 0)

    features = [[ph, moisture, n, p, k]]

    soil = soil_model.predict(features)
    soil_map = {
    "Fertile": t["fertile"],
    "Moderate": t["moderate"],
    "Poor": t["poor"]
}

    soil_name = soil_map.get(soil[0], soil[0])
    crop = crop_model.predict(features)
    crop_map_ta = {
    "Rice": "நெல்",
    "Cotton": "பருத்தி",
    "Wheat": "கோதுமை",
    "Banana": "வாழை",
    "Sugarcane": "கரும்பு",
    "Maize": "மக்காச்சோளம்",
    "Groundnut": "நிலக்கடலை",
    "Turmeric": "மஞ்சள்"
}

    if lang == "ta":
       crop_name = crop_map_ta.get(crop[0], crop[0])
    else:
       crop_name = crop[0] 

    # -------- Crop Rotation Advice --------
    rotation_info = rotation_data[rotation_data["crop"] == crop[0]]
    t = texts[lang]

    if not rotation_info.empty:
        next_crop = rotation_info.iloc[0]["next_crop"]
        soil_effect = rotation_info.iloc[0]["soil_effect"]
        months = rotation_info.iloc[0]["recovery_months"]

        restriction = f"{t['avoid']} {crop[0]} {t['for']} {months} {t['months']}."
        recommendation = f"{t['grow']} {next_crop} {t['restore']}."
        soil_alert = soil_effect

    else:
        restriction = t["follow"]
        recommendation = ""
        soil_alert = ""
        # -------- Nutrient Level Analysis --------
    avg_npk = (n + p + k) / 3
    nutrient_level = "Low"   # default

    if avg_npk < 40:
        nutrient_level = "Low"
    elif avg_npk < 80:
        nutrient_level = "Moderate"
    else:
        nutrient_level = "High"
       # Default English
    nutrient_text = nutrient_level 
        # -------- Fertilizer Advice --------
    if lang == "ta":
        if nutrient_level == "Low":
            nutrient_text = "குறைவு"
        fertilizer = "இயற்கை உரம் மற்றும் NPK உரம் பயன்படுத்தவும்."
    elif nutrient_level == "Moderate":
        nutrient_text = "மிதமானது"
        fertilizer = "சமநிலை உரம் மற்றும் கம்போஸ்ட் பயன்படுத்தவும்."
    else:

   
        nutrient_text = "அதிகம்"
        fertilizer = "அதிக உரம் தேவையில்லை. மண் நிலையை பராமரிக்கவும்."

    # English
    nutrient_text = nutrient_level
   
    if nutrient_level == "Low":
            fertilizer = "Apply organic manure and NPK fertilizers."
    elif nutrient_level == "Moderate":
            fertilizer = "Use balanced fertilizers and compost."
    else:
            fertilizer = "Avoid excess fertilizers. Maintain soil."
    

    
    

    # -------- Save to database --------
    conn = sqlite3.connect("soil.db")
    conn.execute(
        "INSERT INTO soil(ph, moisture, n, p, k, soil, crop) VALUES(?,?,?,?,?,?,?)",
        (ph, moisture, n, p, k, soil[0], crop[0])
    )
    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        soil=soil_name,
        crop=crop_name,
        lang=lang,
        restriction=restriction,
        recommendation=recommendation,
        soil_alert=soil_alert,
        nutrient=nutrient_text,
        fertilizer=fertilizer,
        t=texts[lang]
    )


# ---------------- HISTORY ----------------
@app.route("/history")
def history():
    conn = sqlite3.connect("soil.db")
    data = conn.execute("SELECT * FROM soil").fetchall()
    conn.close()

    return render_template("history.html", data=data)
@app.route("/location")
def location():
    return render_template("location.html")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)