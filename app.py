from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import pandas as pd
import pickle
from sqlalchemy import create_engine
import pymysql

model = pickle.load(open('new_house.pkl', 'rb'))

app = Flask(__name__)

engine_sql = create_engine("mysql+pymysql://root:Swami%401119@localhost:3306/house_price_prediction")


@app.route('/')
def index():
    return render_template('new_house_land.html') # Ensure your HTML file is named index.html

# Predict route (handles form submission)
@app.route("/predict", methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        posted_by = (request.form['posted_by'])
        under_construction = (request.form['under_construction'])
        bhk_no = (request.form['bhk_no'])
        bhk_or_rk = (request.form['bhk_or_rk'])
        square_ft = (request.form['square_ft'])
        ready_to_move = (request.form['ready_to_move'])
        resale = (request.form['resale'])
        longitude = (request.form['longitude'])
        latitude = (request.form['latitude'])
        
        # Prepare input data for the model
        arr = np.array([[posted_by, under_construction, bhk_no, bhk_or_rk, square_ft, ready_to_move, resale, longitude, latitude]])
        prediction = model.predict(arr)


        # Example of inserting into a database (SQLite in this case)
        try:
            with engine_sql.connect() as connection:
                # Create a DataFrame for insertion
                data = {
                    "POSTED_BY": [posted_by],
                    "UNDER_CONSTRUCTION": [under_construction],
                    "BHK_NO": [bhk_no],
                    "BHK_OR_RK": [bhk_or_rk],
                    "SQUARE_FT": [square_ft],
                    "READY_TO_MOVE": [ready_to_move],
                    "RESALE": [resale],
                    "LONGITUDE": [longitude],
                    "LATITUDE": [latitude],
                    "TERGET": [prediction]
                }
                insert_df = pd.DataFrame(data)

                # Insert into MySQL
                insert_df.to_sql(name='house_data', con=connection, if_exists='append', index=False)

                print("Data inserted successfully into 'house_data' table.")

            # Redirect or display a success message
                return render_template('new_house_res.html', prediction = prediction)

        except Exception as e:
            return f"An error occurred: {e}"
        
    return render_template('new_house_res.html', {e})




if __name__ == "__main__":
    app.run(debug=True)
