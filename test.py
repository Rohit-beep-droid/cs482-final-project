import cv2

# Load the webcam
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

mainLoop = True
while mainLoop:

    # gets frame and if it read it
    didRead, currFrame = capture.read()
    if not didRead:
       break
    
    # Display the frame
    cv2.imshow("camera", currFrame)
    
    # HIT ESCAPE TO CLOSE
    if(cv2.waitKey(1) == 27):
        mainLoop = False



capture.release()
cv2.destroyAllWindows()
