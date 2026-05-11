from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect
import pickle
import pandas as pd
import mysql.connector

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="house_db"
)
cursor = db.cursor()

app = Flask(__name__)

model = pickle.load(open('house_model.pkl', 'rb'))



@app.route('/predict', methods=['POST'])
def predict():
    name = request.form['name']
    age = request.form['age']
    contact = request.form['contact']

    area = float(request.form['area'])
    bhk = int(request.form['bhk'])
    bathrooms = int(request.form['bathrooms'])
    floors = int(request.form['floors'])
    parking = int(request.form['parking'])

    city = request.form['city']
    house_type = request.form['house_type']
    furnishing = request.form['furnishing']

    # DB insert
    query = "INSERT INTO users (name, age, contact) VALUES (%s, %s, %s)"
    values = (name, age, contact)
    cursor.execute(query, values)
    db.commit()

    # Prediction
    input_df = pd.DataFrame([{
        'area': area,
        'bhk': bhk,
        'bathrooms': bathrooms,
        'floors': floors,
        'parking': parking,
        'city': city,
        'house_type': house_type,
        'furnishing': furnishing
    }])

    prediction = model.predict(input_df)
    price = int(prediction[0])

    return render_template("index.html", prediction_text=f"Predicted Price: ₹ {price}")


@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "1234":
        return redirect('/home')
    else:
        return "Wrong Username or Password ❌"




if __name__ == "__main__":
    app.run(debug=True)
