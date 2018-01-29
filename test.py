import re
import cv2
import numpy as np
import pytesseract
from PIL import Image
import imutils
from unidecode import unidecode
#from flask import Flask

pytesseract.pytesseract.tesseract_cmd="C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
#app = Flask(__name__)

src_path="C:/Python27/Scripts/pyapp/images/"
#img_path=src_path+"2.png"
#@app.route('/')
def hello():
    img_path = src_path + "bill8.png"
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)


    warped = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 251, 11)




    cv2.imshow("Scanned", imutils.resize(img, height=650))
    cv2.waitKey(0)

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
    result=result.replace('--', '-')
    print result
    date=re.findall(r'(\d+/\d+/\d+)',result)
    date1 = re.findall(r'(\d+-\d+-\d+)', result)
    if len(date)>0:
        dt=date[0]
    elif len(date1)>0:
        dt=date1[0]
    else:
        dt="can't find date"
    total=(re.findall("\d+\.\d+",result))
    t=[float(i) for i in total]
    if len(total)!=0:
        total=max(t)
    else:
        total="can't find total"
    temp=result.split()
    temp1=' '.join(temp)
    list=[]
    for i in temp:
        temp = re.findall(r'^((?![a-zA-Z]*$)[a-zA-Z0-9]+)$', i)
        list.append(temp[0]) if len(temp) > 0 and len(temp[0]) >= 4 else None
    if len(list)>0:
        ino=list[0]
    else:
        ino="can't find invoice no."
    print 'Date:',dt,'\nInvoice no.:',ino,'\n','Total:',total



hello()
#if __name__ == "__main__":
 #   app.run(host="0.0.0.0", debug=True)


