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
image_path = "C://Users/JxH/Documents/Rice Disease Classifier/dataset/IMG_2999.jpg"

# Create an instance of the prediction service
credentials = ApiKeyCredentials(in_headers={"Prediction-key": cv_key})
custom_vision_client = CustomVisionPredictionClient(endpoint=cv_endpoint, credentials=credentials)

# Create a figure to display the results
fig = plt.figure(figsize=(16, 8))

# Get the images and show the predicted classes for each one


# Open the image, and use the custom vision model to classify it
image_contents = open(image_path, 'rb')
classification = custom_vision_client.classify_image(project_id, model_name, image_contents.read())
# The results include a prediction for each tag, in descending order of probability - get the first one
# prediction = classification.predictions[0].tag_name
# prob1 = classification.predictions[0].probability
# prob2 = classification.predictions[1].probability
# prob3 = classification.predictions[2].probability
# prob4 = classification.predictions[3].probability
# # Display the image with its predicted class
# img = Image.open(image_path)
# # a=fig.add_subplot(len(image_path)/3, 3,1)
# # a.axis('off')
# imgplot = plt.imshow(img)
# # a.set_title(prediction)
# # plt.show()
# print(prediction)
# print(prob1)
# print(prob2)
# print(prob3)
# print(prob4)

def predict(x):
    l = []
    for i in range(len(x.predictions)):
        l.append([x.predictions[i].tag_name, x.predictions[i].probability])
    return l


print(predict(classification))

