import base64
import io
from PIL import Image
import numpy as np
import cv2

def file_to_uri(file_object):
    img = Image.open(file_object)
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.getvalue()).decode('ascii')
    mime = "image/jpeg"
    file_url = "data:%s;base64,%s"%(mime, img_base64)
    return file_url

def uri_to_cv(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def cv_to_uri(img):
    buffer = cv2.imencode(".jpg", img)[1]
    rawBytes = io.BytesIO(buffer)
    img_base64 = base64.b64encode(rawBytes.getvalue()).decode('ascii')
    mime = "image/jpeg"
    file_url = "data:%s;base64,%s"%(mime, img_base64)
    return file_url
