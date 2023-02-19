import io
import os
import math

from PIL import Image, ImageDraw, ImageFont

from detect_landmarks import detect_landmarks, detect_properties
from google.cloud import vision
from google.cloud.vision_v1 import types

# set the os GCP App variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=PATH_TO_CREDENTIAL_JSON

# image to send
file_name = os.path.abspath('/Users/yutingyang/Downloads/SP23/HackAI/test.py/landmarks/1.jpeg')

# get image properties
img = Image.open(file_name)
width, height = img.size
I1 = ImageDraw.Draw(img)

# initialize fonts
font1 = ImageFont.truetype('/Library/Fonts/Arial.ttf', int(max(width, height)/50))
font2 = ImageFont.truetype('/Library/Fonts/Arial.ttf', int(min(width, height)/60))

     
# detect color properties
props = detect_properties(file_name)

# draw  dominant color distribution
currentHeight = 0
for color in props.dominant_colors.colors:  
    shape = [(0, currentHeight), (width/8, currentHeight+height*color.pixel_fraction)]
    I1.rectangle(shape, fill=(int(color.color.red), int(color.color.green), int(color.color.blue)))
    currentHeight = height*color.pixel_fraction

# detect landmark     
landmarks = detect_landmarks(file_name)

# print detection results
y1 = 3*height/5
for landmark in landmarks:
    I1.text((3*width/5, y1), landmark.description, font=font1)
    y2 = y1
    for location in landmark.locations:
        lat_lng = location.lat_lng
        y2 += int(max(width, height)/50+10)
        I1.text((3*width/5, y2), 'Latitude {}'.format(lat_lng.latitude), font=font2)
        y2 += int(min(width, height)/60+10)
        I1.text((3*width/5, y2), 'Longitude {}'.format(lat_lng.longitude), font=font2)
    y1 += int(max(width, height)/50+min(width, height)/20)

# display image result
if len(landmarks) != 0:
    img.show()
else:
    print('Error: cannot detect landmark')
