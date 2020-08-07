import cv2
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd= r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image = cv2.imread("C:\\Users\\HD\\PycharmProjects\\untitled\\number-plates-ireland.jpg")
image = imutils.resize(image,width=500)
cv2.imshow('original image',image)
cv2.waitKey(0)

gray =cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("1 - grayscale conversion", gray)
cv2.waitKey(0)

gray = cv2.bilateralFilter(gray, 11,17,17)
cv2.imshow("2- bilateral filter",gray)
cv2.waitKey(0)

edged = cv2.Canny(gray,170,200)
cv2.imshow("3 -canny edges", edged)
cv2.waitKey(0)

cnts, new = cv2.findContours(edged.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

imgl = image.copy()
cv2.drawContours(imgl, cnts, -1, (0,255,0), 3)
cv2.imshow("4 -all contours", imgl)
cv2.waitKey(0)

cnts=sorted(cnts, key= cv2.contourArea, reverse= True)[:30]
NumberPlateCnt = None

img2 = image.copy()
cv2.drawContours(img2, cnts,-1, (0,255,0), 3)
cv2.imshow("5 -top 30 contours", img2)
cv2.waitKey(0)

count =0
idx =7
for c in cnts:
    peri =cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri,True)
    if len(approx) == 4:
        NumberPlateCnt = approx

        x,y,w,h =cv2.boundingRect(c)
        new_img = image[y:y +h, x:x + w]
        cv2.imwrite('C:\\Users\\HD\\PycharmProjects\\untitled\\sanjay'+ str(idx) + '.png', new_img)
        idx+=1

        break

cv2.drawContours(image,[NumberPlateCnt] , -1, (0,255,0), 3)
cv2.imshow("final image with number plate detected", image)
cv2.waitKey(0)

cropped_img_loc = 'C:\\Users\\HD\\PycharmProjects\\untitled\\sanjay7.png'
cv2.imshow("cropped image", cv2.imread(cropped_img_loc))
text = pytesseract.image_to_string(cropped_img_loc, lang='eng')
print("The licence plate number detected is :",text)

cv2.waitKey(0)