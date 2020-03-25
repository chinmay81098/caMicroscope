from flask import Flask,jsonify,request
from flask_cors import CORS
import cv2
import numpy as np
import io
import base64
from PIL import Image
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


CORS(app, resources={r'/*': {'origins': '*'}})

imageFile=""


def splitImage(img):
    arr=[0]*3
    b,g,r = cv2.split(img)
    rgb_img = cv2.merge([r,g,b])
    x,y,z = np.shape(img)
    for i in range(3):
        arr[i] = np.zeros((x,y,z),dtype=int)
        arr[i][:,:,i] = rgb_img[:,:,i]
    return arr

def mergeImages(arr):
    x,y,z = np.shape(arr[0])
    rgb_img = np.zeros((x,y,z),dtype=int)
    for i in range(3):
        b,g,r=cv2.split(arr[i])
        arr[i]=cv2.merge([r,g,b])
        rgb_img[:,:,i] = arr[i][:,:,i]
    return [rgb_img]


@app.route('/response',methods=['GET'])
def response():
    img_arr=[]
    for img in imageFile:
        image = Image.fromarray(img.astype("uint8"))
        rawBytes = io.BytesIO()
        image.save(rawBytes, "JPEG")
        rawBytes.seek(0)
        img_base64 = base64.b64encode(rawBytes.read())
        img_arr.append(str(img_base64))
    return jsonify({'status':img_arr})


@app.route('/merge',methods=["POST"])
def mergeImage():
    global imageFile
    arr=[0]*3
    if request.method == "POST":
        images=request.json
        for i in range(len(images["data"])):
            encoded_data=images["data"][i].split(',')[1]
            arr[i]=np.fromstring(base64.b64decode(encoded_data),np.uint8)
            arr[i]=cv2.imdecode(arr[i],cv2.IMREAD_COLOR)
        imageFile=mergeImages(arr)
    return "Merged!"

@app.route('/sendImage', methods=['POST'])
def upload_image():
    global imageFile
    if request.method == "POST":
        if request.files:
            image = request.files["image"].read()
            npimg = np.fromstring(image,np.uint8)
            img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
            imageFile=splitImage(img)
    else:
        return("Invalid Request")
    return "Success"

if __name__ == '__main__':
    app.run()