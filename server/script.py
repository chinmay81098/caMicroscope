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

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

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
@app.route('/upload-image', methods=['POST'])
def upload_image():
    global imageFile
    if request.method == "POST":
        if request.files:
            image = request.files["image"].read()
            npimg = np.fromstring(image,np.uint8)
            img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
            #blueChannel,greenChannel,redChanel = cv2.split(img)
            #imageFile=[blueChannel,greenChannel,redChanel]
            b,g,r = cv2.split(img)
            rgb_img = cv2.merge([r,g,b])
            x,y,z = np.shape(img)
            red = np.zeros((x,y,z),dtype=int)
            green = np.zeros((x,y,z),dtype=int)
            blue = np.zeros((x,y,z),dtype=int)
            for i in range(0,x):
                for j in range(0,y):
                    red[i][j][0] = rgb_img[i][j][0]
                    green[i][j][1] = rgb_img[i][j][1]
                    blue[i][j][2] = rgb_img[i][j][2]
            imageFile=[red,green,blue] 
    return "success"

if __name__ == '__main__':
    app.run()