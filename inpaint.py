import cv2

def inpaint(image, mask, radius=3, method=cv2.INPAINT_TELEA):
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    output = cv2.inpaint(image, mask, radius, method)
    return output