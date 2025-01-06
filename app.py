from flask import Flask
from flask import render_template
import pickle
import numpy as np
from flask import request

model = pickle.load(open('new_house.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('new_house_land.html')

@app.route("/predict", methods=['POST', 'GET'])
def predict():
    try:
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
        

        return render_template('new_house_res.html', prediction = prediction)
    except Exception as e:
        return render_template('new_house_res.html', error=str(e))


if __name__=="__main__":
    app.run(debug=True)

