from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np 
from flask import Flask, render_template, request, jsonify
import os
import cv2
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# Function to process the image with your AI model
def process_image(image_path):
    # Load the image
    model_path = 'static/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5'
    model=load_model(model_path,compile=False)
    # if os.path.exists(image_file):
    #     img = image.load_img(image_file, target_size=(64, 64))
    #     imag = image.img_to_array(img)
    #     imaga = np.expand_dims(imag, axis=0)
    #     ypred = model.predict(imaga)
    #     if ypred[0] == 1:
    #         result = {'output':'detected'}
    #         return result
    #     else:
    #         result = {'output':'not detected'}
    #         return result
    # else:
    #     result =  {'output':'image file not found'}
    #     return result

# def predict_image(image_path, model=model):
    img = cv2.imread(image_path)
    img_resized = cv2.resize(img, (img_width, img_height))
    img_resized = img_resized / 255.0
    img_resized = np.expand_dims(img_resized, axis=0)
    prediction = model.predict(img_resized)
    predicted_label = np.argmax(prediction)
    class_names = ['PNEUMONIA', 'TUBERCULOSIS', 'NORMAL']
    predicted_class = class_names[predicted_label]
    result ={'output':predicted_class}
    return result 

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the uploaded image
        if 'image' not in request.files:
            return jsonify({'error': 'No image found'})
        uploaded_image = request.files['image']
        uploaded_image_path = 'uploads/' + uploaded_image.filename
        uploaded_image.save(uploaded_image_path)
        result = process_image(uploaded_image_path)
        return render_template('result.html', result=result)
    return render_template('upload_form.html')



if __name__ == '__main__':
    app.run(debug=True)
