from flask import Flask, render_template, request
import pickle
import joblib
import numpy as np
import sklearn

app = Flask(__name__)

# Load the model from the pickle file
with open('scaler_model.pkl', 'rb') as file:
    scaler = joblib.load(file)

with open("Logistic_prediction.pkl", 'rb') as file:
    model = joblib.load(file)

with open("Random_Forest_Classifier.pkl", 'rb') as file:
    forest_classifier = joblib.load(file)


@app.route('/')
def index():
    return render_template('prediction-form.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None
    if request.method == 'POST':
        name = request.form['name']
        sex = int(request.form['sex'])
        urban_rural = int(request.form['urban_rural'])
        income = request.form['income']
        gpa = float(request.form['gpa'])
        parents_qualification = request.form['parents_qualification']
        attendance = float(request.form['attendance'])

        gpa_avg = scaler.transform([[gpa, attendance]])
        if income == "Low":
            income_input = [1, 0]
        elif income == "Medium":
            income_input = [0, 1]
        else:
            income_input = [0, 0]

        if parents_qualification == "Illiterate":
            quali_input = [1, 0]
        elif parents_qualification == "High School":
            quali_input = [0, 1]
        else:
            quali_input = [0, 0]

        to_be_predicted = [gpa_avg[0][0], gpa_avg[0][1], sex, urban_rural, income_input[0], income_input[1],
                           quali_input[0], quali_input[1]]
        prediction = model.predict_proba([to_be_predicted])
        print(model.coef_)

        if prediction[0][1]>=0.71:
            prediction = "Dropout"
        else:
            prediction = "No Dropout"

        # Preprocess input data
        # input_data = preprocess_input(name, sex, urban_rural, income, gpa, parents_qualification, attendance)

        # Predict dropout probability
        dropout_probability = 100

        # Render the result template
        return render_template('prediction-form.html', name=name, dropout_probability=prediction)


if __name__ == '__main__':
    app.run(debug=True)
