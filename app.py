from flask import Flask, request, render_template, redirect, url_for, jsonify
import numpy as np
import pandas as pd
import pickle
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('C:/Users/kulka/OneDrive/Desktop/House price prediction/house-price-prediction-8013d-firebase-adminsdk-fbsvc-4c147efdd7.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://house-price-prediction-8013d-default-rtdb.asia-southeast1.firebasedatabase.app/'})



model = pickle.load(open('new_house.pkl', 'rb'))

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('new_house_land.html') # Ensure your HTML file is named index.html

# Predict route (handles form submission)
@app.route("/predict", methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        posted_by = request.form['posted_by']
        under_construction = request.form['under_construction']
        bhk_no = request.form['bhk_no']
        bhk_or_rk = request.form['bhk_or_rk']
        square_ft = request.form['square_ft']
        ready_to_move = request.form['ready_to_move']
        resale = request.form['resale']
        longitude = request.form['longitude']
        latitude = request.form['latitude']
        
        # Prepare input data for the model
        arr = np.array([[posted_by, under_construction, bhk_no, bhk_or_rk, square_ft, ready_to_move, resale, longitude, latitude]], dtype= float)
        prediction = model.predict(arr)


        # Example of inserting into a database (SQLite in this case)
        try:
            ref = db.reference('predictions')
            ref.push({
                'posted_by' : posted_by,
                'under_construction' : under_construction,
                'bhk_no' : bhk_no,
                'bhk_or_rk' : bhk_or_rk,
                'square_ft' : square_ft,
                'ready_to_move' : ready_to_move,
                'resale' : resale,
                'longitude' : longitude,
                'latitude' : latitude,
                'predicted_price': float(prediction[0])
            })

            #return jsonify({'message': 'Data saved successfully!'}), 200

            # Redirect or display a success message
            return render_template('new_house_res.html', prediction = prediction)

        except Exception as e:
            return f"An error occurred: {e}"
        
    return render_template('new_house_res.html', {e})




if __name__ == "__main__":
    app.run(debug=True)
