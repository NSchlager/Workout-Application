from flask import Flask, render_template, request, redirect
import csv
import os
from datetime import date
import ctypes
import csv_reader
import requests

app = Flask(__name__)
CSV_FILE = "workouts.csv"

CALORIE_CSV = "calories.csv"



#reps = csv_reader.read_column_from_csv('workouts.csv', 'reps')

#load the shared c library
#lib = ctypes.CDLL('./libsum.dll')

#Tells python the argument types and return type of the C function of sum_array.
#lib.sum_array.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
#lib.sum_array.restype = ctypes.c_double

#Tells python the argument types and return type of the C function of one_rep_max.
#lib.one_rep_max.argtypes = [ctypes.c_double, ctypes.c_int]
#lib.one_rep_max.restype = ctypes.c_double

#arr = (ctypes.c_double * len(reps))(*reps)
#result = lib.sum_array(arr, len(reps))
#print("Sum of total money among friends: %.2f" % result)
def init_calorie_csv():
    if not os.path.exists(CALORIE_CSV):
        with open(CALORIE_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "meal", "food", "calories"])
init_calorie_csv()

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "exercise", "sets", "reps", "weight"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan")
def scan():
    return render_template("scan.html")


@app.route("/lookup-barcode")
def lookup_barcode():
    barcode = request.args.get("barcode", "").strip()
    if not barcode:
        return {"error": "No barcode provided"}, 400

    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "WorkoutLogger/1.0"})
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}, 500

    if response.status_code != 200:
        return {"error": f"API returned status {response.status_code}"}, 502

    try:
        data = response.json()
    except ValueError:
        return {"error": "Invalid response from API"}, 502

    if data.get("status") != 1:
        return {"error": "Product not found"}, 404

    product = data["product"]
    nutriments = product.get("nutriments", {})

    print("Nutriments:", nutriments)  # debug: see every nutrient field available

    name = product.get("product_name", "Unknown")

    # Try several possible field names, in order of preference
    calories = (
        nutriments.get("energy-kcal_100g")
        or nutriments.get("energy-kcal_serving")
        or nutriments.get("energy_100g")
        or nutriments.get("energy_value")
    )

    return {
        "name": name,
        "calories_per_100g": calories,
        "brand": product.get("brands", "")
    }


@app.route("/calories")
def calories():
    prefill_food = request.args.get("food", "")
    prefill_calories = request.args.get("calories", "")
    date_filter = request.args.get("date", "").strip()

    entries = []
    if os.path.exists(CALORIE_CSV):
        with open(CALORIE_CSV, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if date_filter and row["date"] != date_filter:
                    continue
                entries.append(row)

    entries.sort(key=lambda r: r["date"], reverse=True)

    total_calories = sum(float(e["calories"]) for e in entries) if entries else 0
    today_str = str(date.today())
    today_calories = sum(
        float(e["calories"]) for e in entries if e["date"] == today_str
    ) if not date_filter else None

    return render_template(
        "calories.html",
        entries=entries,
        total_calories=round(total_calories, 1),
        today_calories=round(today_calories, 1) if today_calories is not None else None,
        date_filter=date_filter,
        prefill_food=prefill_food,
        prefill_calories=prefill_calories
    )

if __name__ == "__main__":
    init_csv()
    app.run(debug=True)