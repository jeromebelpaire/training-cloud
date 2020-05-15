import pickle
import Utils.calculateFeatures as calculateFeatures
import Utils.dataCleaning as dataCleaning
import Utils.dataReading as dataReading
import sys
import os
import json
import pandas as pd
currentDirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(currentDirPath)+"/Utils")


# function that predicts author of a file or a collection of files based on a path:
def predictAuthor(predictionModel, filePath=None, folderPath=None, directText=None):
    if filePath:
        documentsData = dataReading.readTextFiles(
            filePath=filePath, lower=True, parseIDAuthorName=False)
    if folderPath:
        documentsData = dataReading.readTextFiles(
            folderPath=folderPath, lower=True, parseIDAuthorName=False)
    if directText:
        documentsData = pd.DataFrame([directText.lower()], columns=["text"])
        documentsData["path"] = "Not applicable"

    inputDataDict = documentsData.to_dict("list")

    # Step 2: Pre-cleaning feature calculation: some feautures have to be calculated before cleaning (ex: number of special characters, named entities, ...):
    documentsData = calculateFeatures.fullFeatureCalculation(pdDataFrame=documentsData,
                                                             textColumnName="text",
                                                             applyTextLength=True,
                                                             applyPunctiationMeasures=True,
                                                             applyCountByNamedEntityType=True,
                                                             applyNumberOfWords=True,
                                                             applyNumberOfStopWords=True,
                                                             applyAvgWordLength=True,
                                                             applyNumberOfNumerics=True,
                                                             applySentiment=True,
                                                             applyTfIdf=False)

    print("finished step 2: Calculating pre-cleaning features")

    # Step 3: Cleaning: now that pre-cleaning features are calculated, cleaning can be applied:
    documentsData = dataCleaning.fullDataCleaning(pdDataFrame=documentsData,
                                                  textColumnName="text",
                                                  # sadly enough too time consuming for my computer..
                                                  corrSpelling=False,
                                                  repContractions=True,
                                                  remPunctuation=True,
                                                  lemmatize=True,
                                                  delStopWords=True)

    print("finished step 3: Cleaning the text data")

    # step 4: apply feature engeneering that need to be applied on cleaned data (IDF) fromloaded IDF model (to maintain same vocab list):
    documentsData["TfIdf"] = calculateFeatures.TfIdf(pandasColumn=documentsData["text"], modelLoadPath=os.path.dirname(
        currentDirPath) + "/Models/TFIDF Model/tfidfmodel.pkl")

    # All tfidf values are contained in one column (column where each cell is a list of values). We will transform that to multople columns:

    splittedTfIdf = pd.DataFrame(documentsData["TfIdf"].values.tolist())
    documentsData = pd.concat([documentsData, splittedTfIdf], axis=1)
    del documentsData["TfIdf"]

    # Step 5: prediction:

    # deleting unnecessary cols:
    del documentsData["text"]
    del documentsData["path"]

    outputDict = {"input": inputDataDict,
                  "predicted authors": predictionModel.predict(documentsData[predictionModel.feature_names]).tolist()}

    return json.dumps(outputDict, indent=2, sort_keys=True)


if __name__ == '__main__':
    # load trained prediction nmodel:
    with open(os.path.dirname(currentDirPath) + "/Models/bestPerformingModel/bestPerformingModel.pkl", 'rb') as file:
        predictionModel = pickle.load(file)

    folderPath = os.path.dirname(currentDirPath) + "/Data/inputFilesExamples"
    filePath = folderPath+"/doc_id00003testMultiLine.txt"

    print("Testing function referring to single file:")
    print(predictAuthor(predictionModel=predictionModel, filePath=filePath))

    print("Testing function referring to folder:")
    print(predictAuthor(predictionModel=predictionModel, folderPath=folderPath))

    print("Testing function giving directly text as input:")
    print(predictAuthor(predictionModel=predictionModel,
                        directText="Cloud is the future"))
