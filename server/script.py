from flask import Flask,jsonify,request
from flask_cors import CORS
import cv2
import numpy

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
    return jsonify({
        'error':'false',
        'message':'helloworld',
    })
@app.route('/upload-image', methods=['POST'])
def upload_image():
    global imageFile
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            imageFile = cv2.imdecode(numpy.fromstring(image.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    return

if __name__ == '__main__':
    app.run()