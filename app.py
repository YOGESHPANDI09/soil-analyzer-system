from flask import Flask, render_template, request
import sqlite3
import joblib

app = Flask(__name__)

# =========================
# LOAD ML MODELS
# =========================
soil_model = joblib.load("soil_model.pkl")
crop_model = joblib.load("crop_model.pkl")


# =========================
# LANGUAGE DICTIONARY
# =========================
texts = {
    "en": {
        "title": "🌱 Soil Analyzer System",
        "ph": "pH Value",
        "moisture": "Moisture (%)",
        "n": "Nitrogen",
        "p": "Phosphorus",
        "k": "Potassium",
        "analyze": "Analyze Soil",
        "history": "History",
        "soil": "Soil Type",
        "crop": "Recommended Crop",
        "back": "Back"
    },
    "ta": {
        "title": "🌱 மண் ஆய்வு முறை",
        "ph": "pH மதிப்பு",
        "moisture": "ஈரப்பதம்",
        "n": "நைட்ரஜன்",
        "p": "பாஸ்பரஸ்",
        "k": "பொட்டாசியம்",
        "analyze": "மண் பரிசோதனை",
        "history": "வரலாறு",
        "soil": "மண் வகை",
        "crop": "பரிந்துரைக்கப்பட்ட பயிர்",
        "back": "திரும்ப"
    }
}


# =========================
# DATABASE
# =========================
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


# =========================
# HOME
# =========================
@app.route("/")
def home():
    lang = request.args.get("lang", "en")
    return render_template("index.html", t=texts[lang], lang=lang)


# =========================
# ANALYZE (ML)
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():

    lang = request.args.get("lang", "en")

    ph = float(request.form["ph"])
    moisture = float(request.form["moisture"])
    n = float(request.form["n"])
    p = float(request.form["p"])
    k = float(request.form["k"])

    features = [[ph, moisture, n, p, k]]

    soil = soil_model.predict(features)[0]
    crop = crop_model.predict(features)[0]

    conn = sqlite3.connect("soil.db")
    conn.execute(
        "INSERT INTO soil(ph, moisture, n, p, k, soil, crop) VALUES(?,?,?,?,?,?,?)",
        (ph, moisture, n, p, k, soil, crop)
    )
    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        soil=soil,
        crop=crop,
        t=texts[lang],
        lang=lang
    )


# =========================
# HISTORY
# =========================
@app.route("/history")
def history():

    lang = request.args.get("lang", "en")

    conn = sqlite3.connect("soil.db")
    data = conn.execute("SELECT * FROM soil").fetchall()
    conn.close()

    return render_template(
        "history.html",
        data=data,
        t=texts[lang],
        lang=lang
    )


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)
