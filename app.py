import cv2
import numpy as np
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)


def remove_watermark(image):
    img = cv2.imread(image)
    resized_img = cv2.resize(img, (0, 0), fx=0.2, fy=0.2)
    copy_img = img.copy()
    copy_img[:] = (255, 255, 255)
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    resized_imghsv = cv2.resize(imghsv, (0, 0), fx=0.2, fy=0.2)

    # Menentukan rentang warna merah pada skala HSV
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    # Membuat mask untuk range warna merah
    red_mask = cv2.inRange(imghsv, lower_red, upper_red)

    # Menentukan rentang warna biru pada skala HSV
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    # Membuat mask untuk range warna biru
    blue_mask = cv2.inRange(imghsv, lower_blue, upper_blue)

    # Menggabungkan kedua mask
    mask = cv2.bitwise_or(red_mask, blue_mask)

    res_white = cv2.bitwise_and(copy_img, copy_img, mask=mask)
    res = cv2.add(img, res_white)
    resized_res = cv2.resize(res, (0, 0), fx=0.2, fy=0.2)

    cv2.imwrite('hasil.jpg', resized_res)
    return 'hasil.jpg'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(filename)
    result = remove_watermark(filename)
    return download(result)


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run()
