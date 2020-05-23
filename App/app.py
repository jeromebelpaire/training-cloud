from flask import Flask, render_template, request
from Scripts.predictFunction import predictAuthor
import pickle
import os


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check currentdir
        currentDirPath = os.path.dirname(os.path.realpath(__file__))

        input_text = request.form.get('input_text')

        if len(input_text) > 0:
            # load trained prediction nmodel:
            with open(os.path.dirname(currentDirPath) + "/Models/bestPerformingModel/bestPerformingModel.pkl", 'rb') as file:
                predictionModel = pickle.load(file)

            result = predictAuthor(predictionModel=predictionModel,
                                   directText=input_text)
            predicted_author = eval(result)["predicted authors"][0]
        else:
            predicted_author = 'Could not predict empty text'

    else:
        input_text = ''
        predicted_author = ''
    return render_template('index.html',
                           input_text=input_text,
                           prediction=predicted_author)


if __name__ == "__main__":
    app.run(debug=True,
            # host='0.0.0.0',
            port='80')
