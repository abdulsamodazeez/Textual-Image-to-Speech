from page_transform.transform import four_point_transform
from skimage.filters import threshold_local
from glob import glob as glob

import cv2
import imutils
import pytesseract
import pyttsx3


#Recognized printed text from a page using OpenCV and PyTesseract
def edge_recognize_printed_page(image):
    # load the image and compute the ratio of the old height to the new height,
    # clone it, and resize it
    print("Load image at" + image)
    image = cv2.imread(image)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    screenCnt = None

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    # apply the four point transform to obtain a top-down view of the
    # original image
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset = 10, method = "gaussian")
    warped = (warped > T).astype("uint8") * 255

    # Recognize printed text using PyTesseract
    print("Recognizing Text...")
    text = pytesseract.image_to_string(warped)
    print("Recognized Text:\n\n" + text)

    # Speak the recognized text using pyttsx3
    print("Speaking Text")
    
    
    def speak(text):
      engine = pyttsx3.init()
      rate = engine.getProperty('rate')
      engine.setProperty('rate', 125)
      voices = engine.getProperty('voices')
      engine.setProperty('voice', voices[0].id)
      engine.say(text)
      engine.runAndWait()
    return speak(text)


# Recognized printed text from a book using OpenCV and PyTesseract
def edge_recognize_printed_book(image):
    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    print("Load image at" + image)
    image = cv2.imread(image)
    
    orig = image.copy()
    image = imutils.resize(image, height = 500)

    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    orig = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    T = threshold_local(orig, 11, offset = 10, method = "gaussian")
    orig = (orig > T).astype("uint8") * 255

    # Recognize printed text using PyTesseract
    print("Recognizing Text...")
    text = pytesseract.image_to_string(orig)
    print("Recognized Text:\n\n" + text)

    # Speak the recognized text using pyttsx3
    print("Speaking Text")
    

   
    def speak(text):
      engine = pyttsx3.init()
      rate = engine.getProperty('rate')
      engine.setProperty('rate', 125)
      voices = engine.getProperty('voices')
      engine.setProperty('voice', voices[0].id)
      engine.say(text)
      engine.runAndWait()
    return speak(text)

# Recognize printed text on the edge
def edge_print_read():
    # First, try to recognized text from a page. If no page was detected,
    # then recognize text from a book
    try:
        
        edge_recognize_printed_page(save_image_path)
    except:
        edge_recognize_printed_book(save_image_path)
        

edge_print_read()
