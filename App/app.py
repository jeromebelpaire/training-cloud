from flask import Flask, render_template
from Scripts.predictFunction import predictAuthor
import os
import pickle

app = Flask(__name__)


@app.route('/')
def index():
    # Check currentdir
    currentDirPath = os.path.dirname(os.path.realpath(__file__))

    # load trained prediction nmodel:
    with open(os.path.dirname(currentDirPath) + "/Models/bestPerformingModel/bestPerformingModel.pkl", 'rb') as file:
        predictionModel = pickle.load(file)

    result = predictAuthor(predictionModel=predictionModel,
                           directText="Cloud is the future")
    predicted_author = eval(result)["predicted authors"][0]
    return render_template('index.html', prediction=predicted_author)


if __name__ == "__main__":
    app.run(debug=True)
