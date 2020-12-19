from flask import Flask, render_template, request, jsonify, after_this_request
import numpy as np
import sklearn
import pickle
import pandas as pd


PATH = 'insurance_model.pkl' 
model = pickle.load(open(PATH, 'rb'))

app = Flask(__name__) #creating an insance of flask

@app.route('/',  methods=['POST', 'GET']) #a route that defines where the page is going
def home():
    if request.method == 'POST':

        female = 0
        male = 0
        smoker_no = 0
        smoker_yes = 0
        region_ne = 0
        region_nw = 0
        region_se = 0
        region_sw = 0

        age = request.form['age']
        bmi = request.form['bmi']
        children = request.form['children']
        gender = request.form['gender']
        smoking = request.form['smoking']
        region = request.form['region']

        if not age or not bmi or not children:
            return render_template('index.html', content='Invalid - fill out all boxes')

        if gender == 'female':
            female = 1
        else:
            male = 1
        if smoking == 'no':
            smoker_no = 1
        else:
            smoker_yes = 1
        if 'rne' in region:
            region_ne = 1
        elif 'rnw' in region:
            region_nw = 1
        elif 'rse' in region:
            region_se = 1
        else:
            region_sw = 1
        
        pred = model.predict([[age, bmi, children, female, male, smoker_no, smoker_yes, region_ne, region_nw, region_se, region_sw]])
        content = '$' + str(round(pred[0], 2))

        return render_template('index.html', content=content)
    return render_template('index.html')



if __name__ == "__main__":
    app.run()


