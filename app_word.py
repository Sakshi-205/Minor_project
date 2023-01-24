import os
# import cv2
# import keras.utils as krs
# import numpy as np
# import pandas as pd
# import tensorflow as tf
import shutil
from flask import Flask, request, render_template
import subprocess

UPLOAD_FOLDER = 'static/uploads'

# model_best = tf.keras.models.load_model('content/model_final.h5')

# classDict = {
#             0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A",
#             11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K",
#             21: "L", 22: "M", 23: "N", 24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U",
#             31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z", 36: "a", 37: "b", 38: "c", 39: "d", 40: "e",
#             41: "f", 42: "g", 43: "h", 44: "i", 45: "j", 46: "k", 47: "l", 48: "m", 49: "n", 50: "o",
#             51: "p", 52: "q", 53: "r", 54: "s", 55: "t", 56: "u", 57: "v", 58: "w", 59: "x", 60: "y",
#             61: "z"}






def predict_class(model, images):
    images = UPLOAD_FOLDER + '/' + images
    print(images)

    # img = images
    # test_image = krs.load_img(img, target_size=(64, 64))
    # test_image = krs.img_to_array(test_image)
    # test_image = np.expand_dims(test_image, axis=0)
    # result = model.predict(test_image)

    # outputDf = pd.DataFrame(result)
    # maxIndex = list(outputDf.idxmax(axis=1))
    # print("Max index: ", maxIndex)

    # a = maxIndex[0]

    # img_pred = classDict.get(a, "error")
    # return img_pred

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
#
@app.route('/')
def index():
    img = 'static/profile.jpg'
    return render_template('index.html', img=img)
#
#
@app.route('/recognize')
def magic():
    for i in os.listdir('static/uploads'):
        os.remove('static/uploads/' + i)
    return render_template('recognize.html')


@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("img")
    for f in files:
        f.save('static/uploads/' + f.filename)

    return render_template('recognize.html')


@app.route('/update', methods=['POST'])
def update():
    return render_template('index.html', img='static/P2.jpg')
#
#
@app.route('/predict')
def predict():
    images = os.listdir('static/uploads')
    #print(images)
    i = 0

    # predicted = predict_class(model_best, images[0])
    # print("cp static/uploads/" + images[0] + " SimpleHTR/data/word.png")
    # subprocess.call("cp static/uploads/" + images[0] + " SimpleHTR/data/word.png", shell=True)
    shutil.copy("static/uploads/" + images[0], "SimpleHTR/data/")
    os.chdir("SimpleHTR/data/")
    
    if os.path.exists("word.png") :
        os.remove("word.png")

    os.rename(images[0], "word.png")
    os.chdir("../src/")

    # subprocess.call("python main.py", shell=True)
    result = subprocess.run(["python", "main.py"], stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8")
    lines  = result.split("\n")
    print("  ")
    print("  ")
    predicted = [line for line in lines if 'Recognized:' in line]
    predicted = str(predicted[0])
    predicted = predicted.string("Recognized:")
    print([line for line in lines if 'Recognized:' in line])
    print("  ")
    print("  ")
    # subprocess.run(["python", "SimpleHTR/src/main.py"])
    # process = Popen(['main', 'SimpleHTR/src/main.py'], stdout=PIPE, stderr=PIPE)
    # stdout, stderr = process.communicate()

    # print(stdout)
    print('check')
    # print(predicted)


    return render_template('results.html', result=predicted)

#
if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='127.0.0.1')
    @click.argument('PORT', default=5000, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using
            python server.py
        Show the help text using
            python server.py --help
        """
        HOST, PORT = host, port
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
    run()
