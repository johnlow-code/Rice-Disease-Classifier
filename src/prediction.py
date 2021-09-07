from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import matplotlib.pyplot as plt
from PIL import Image
import os

project_id = '4d2f151e-7d72-4cb3-8512-9a3a7e43f26e'
cv_key = 'e9b017ef95734a6ebef8ab317607b19c'
cv_endpoint = 'https://southeastasia.api.cognitive.microsoft.com/'

model_name = 'RiceDiseaseClassifier' # this must match the model name you set when publishing your model iteration (it's case-sensitive)!
print('Ready to predict using model {} in project {}'.format(model_name, project_id))


# Get the test images from the data/vision/test folder
image_path = "D:\John Low\Programming\Python\Rice-Disease-Classifier\dataset\IMG_2999.jpg"

# Create an instance of the prediction service
credentials = ApiKeyCredentials(in_headers={"Prediction-key": cv_key})
custom_vision_client = CustomVisionPredictionClient(endpoint=cv_endpoint, credentials=credentials)

# Create a figure to display the results
fig = plt.figure(figsize=(16, 8))

# Get the images and show the predicted classes for each one


# Open the image, and use the custom vision model to classify it
image_contents = open("D:\John Low\Programming\Python\Rice-Disease-Classifier\dataset\IMG_2999.jpg", 'rb')
classification = custom_vision_client.classify_image(project_id, model_name, image_contents.read())
# The results include a prediction for each tag, in descending order of probability - get the first one
prediction = classification.predictions[0].tag_name
# Display the image with its predicted class
img = Image.open("D:\John Low\Programming\Python\Rice-Disease-Classifier\dataset\IMG_2999.jpg")
a=fig.add_subplot(len(image_path)/3, 3,i+1)
a.axis('off')
imgplot = plt.imshow(img)
a.set_title(prediction)
plt.show()