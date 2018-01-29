import re
import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
from unidecode import unidecode

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


# img_path=src_path+"2.png"

# @app.route('/')
# def index():
#     return 'Hello World!'

@app.route('/ocr', methods=['GET'])
def hello():
    # print tesserocr.tesseract_version()
    # subprocess.check_output("C:/cygwin/bin/bash.exe ./
    # os.chdir("C:/Python27/Scripts/pyapp/images/")
    # pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
    src_path = "/code/images/"
    # for i in range(5,12,8):
    os.system("bash -c \"./textcleaner -g -e none -f  12 -o 5 ./images/bill5.png ./images/out.jpg\"")
    img_path = src_path + "out.jpg"
    # Read image with opencv
    img = cv2.imread(img_path)
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    warped = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 251, 11)

    # show the original and scanned images
    # print("STEP 3: Apply perspective transform")

    # cv2.imshow("Scanned", imutils.resize(warped, height=650))
    # cv2.waitKey(0)
    # Write image after removed noise
    cv2.imwrite(src_path + "removed_noise.png", warped)

    #  Apply threshold to get image with only black and white
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + "thres.png", warped)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))

    # Remove template file
    # os.remove(temp)

    result = unidecode(result)
    result = result.replace('--', '-')
    print result

    dt = getDate(result)

    total = getTotal(result)

    ino = getInvoiceNumber(result)

    res = {'date': dt, 'invoice_no': ino, 'total': total}

    return jsonify(res)


def getDate(result):
    date = re.findall(r'\d+/\d+/\d+', result)
    date1 = re.findall(r'\d+-\d+-\d+', result)
    date2 = re.findall(r'\d+\-[A-Za-z]+\-\d+', result)
    if len(date) > 0:
        return date[0]
    elif len(date1) > 0:
        return date1[0]
    elif len(date2) > 0:
        return date2[0]
    return "can't find date"


def getInvoiceNumber(result):
    temp = result.split()
    # temp1 = ' '.join(temp)
    list = []
    for i in temp:
        temp = re.findall(r'^((?![a-zA-Z]*$)[a-zA-Z0-9]+)$', i)
        list.append(temp[0]) if len(temp) > 0 and len(temp[0]) >= 4 else None
    if len(list) > 0:
        return list[0]
    else:
        return "can't find invoice no."


def getTotal(result):
    total = (re.findall("\d+\.\d+", result))
    total1 = (re.findall("\d\,\d+\.\d+", result))
    if len(total1) != 0:
        for i in total1:
            total.append(i.replace(",", ""))
    # print "im total",total,total1
    t = [float(i) for i in total]
    if len(total) != 0:
        return max(t)

    else:
        return "can't find total"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
