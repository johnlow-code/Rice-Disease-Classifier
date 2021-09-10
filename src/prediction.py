from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import matplotlib.pyplot as plt
from numpy import round


def predict(image_path):
    project_id = '139db08d-0621-48b7-b9da-51c132d04b45'
    cv_key = 'e9b017ef95734a6ebef8ab317607b19c'
    cv_endpoint = 'https://southeastasia.api.cognitive.microsoft.com/'

    model_name = 'RiceDiseaseClassifier2'  # this must match the model name you set when publishing your model iteration (it's case-sensitive)!
    print('Ready to predict using model {} in project {}'.format(model_name, project_id))

    # Get the test images from the data/vision/test folder

    # Create an instance of the prediction service
    credentials = ApiKeyCredentials(in_headers={"Prediction-key": cv_key})
    custom_vision_client = CustomVisionPredictionClient(endpoint=cv_endpoint, credentials=credentials)

    # Create a figure to display the results
    fig = plt.figure(figsize=(16, 8))

    # Get the images and show the predicted classes for each one

    # Open the image, and use the custom vision model to classify it
    image_contents = open(image_path, 'rb')
    classification = custom_vision_client.classify_image(project_id, model_name, image_contents.read())

    results = []
    for i in range(len(classification.predictions)):
        results.append(
            [classification.predictions[i].tag_name, round(classification.predictions[i].probability * 100, 2)])

    return results
