# This is our code for the eye tracking with help from various sources and Chat Gpt

#Project Creators:
# Matthew Doyle, Rohit Barua, and Nikhil Arora

import cv2
import time

print("Welcome to Our Final Project")
platform = 0

try: 
    platform = int(input("Please Enter Your OS:\nWindows -- 0\nOther ---- 1\nEnter Number Here: "))
    if(not(platform == 0 or platform == 1)):
        raise Exception
except:
    print("WHY YOU GOTTA DO THAT!")
    print("Shutting Down")
    exit()

# Load in the trained data using open cv cascade classifier
# The date was told to us by Chat Gpt at this link:
# https://github.com/anaustinbeing/haar-cascade-files/blob/master/haarcascade_eye.xml
eyeData = cv2.CascadeClassifier('haarcascade_eye.xml')

# Start the webcam
scrnCap = cv2.VideoCapture(platform)

# Loop Variable
running = True

# looking at camera
looking = False

# Time vars
timeLooking = 0;
timeNotLooking = 0;
startTime = 0

# Start the timer
startTime = time.time()

# run until exited out
while running:

    # Grab the current frame
    # based on documentation
    # https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html
    frameRead, currFrame = scrnCap.read()

    # convert the color to grayscale to make circle detection easier
    # https://www.geeksforgeeks.org/python-grayscaling-of-images-using-opencv/
    grayScale = cv2.cvtColor(currFrame, cv2.COLOR_BGR2GRAY)


    # Find the eyes that are in the frame
    # Understanding of this came from:
    # https://stackoverflow.com/questions/20801015/recommended-values-for-opencv-detectmultiscale-parameters
    eyeList = eyeData.detectMultiScale(grayScale, scaleFactor=1.2, minNeighbors=5, minSize = [65,65])


    # ----See if the eye is looking at the camera----
    circles = None
    # Loop through the eyes
    for (xPos, yPos, width, height) in eyeList:

        # Pulled from AI
        # Set up a smaller image consisting only of the eye to detect later
        eye_roi_gray = grayScale[yPos:yPos+height, xPos:xPos+width]

        # Finds the circles in the eye area if it finds one close enough it counts it as looking
        # Inspired By this: 
        # https://stackoverflow.com/questions/39167828/eye-pupil-tracking-using-hough-circle-transform
        circles = cv2.HoughCircles(eye_roi_gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

        # Get center
        eyeCenter = [int(xPos + width/2), int(yPos + height/2)]

        # Get radius
        eyeRadius = int(eyeCenter[0] - xPos)

        # Draw a circle
        cv2.circle(currFrame,eyeCenter,eyeRadius, (0,0,0), 1)
        

    # If a circle is detected, the eye should be looking at the camera
    if circles is not None:
        # looking at the camera
        cv2.putText(currFrame, "Currently Looking at Camera :)", (80, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)     

        # Calculate time looking
        timeLooking = timeLooking + (time.time() - startTime)


    else:
        # not looking at the camera
        cv2.putText(currFrame, "Not Looking at Camera :(", (120, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)      

        # Calculate time not looking
        timeNotLooking = timeNotLooking + (time.time() - startTime)

    # Start the timer back up
    startTime = time.time()

    
    # Display the resulting frame
    cv2.imshow('Eye Detection', currFrame)    

    # Check if we need to exit 
    # (Pulled from Stack overflow: https://stackoverflow.com/questions/13307606/closing-video-window-using-close-x-button-in-opencv-python)
    exitKey = cv2.waitKey(1)
    if cv2.getWindowProperty('Eye Detection', cv2.WND_PROP_VISIBLE) <1 or exitKey == 27:
        running = False



# Release the webcam and close the window
scrnCap.release()
cv2.destroyAllWindows()


# Print the statistics
print("\n-------------------------------------")
timeNotLooking = round(timeNotLooking, 2)
timeLooking = round(timeLooking, 2)
print(f"Time Looking {timeLooking} seconds")
print(f"Time Not Looking {timeNotLooking} seconds")
print(f"Percentage Looking at the camera {round((timeLooking / (timeLooking + timeNotLooking) * 100), 2)}%")
print("-------------------------------------")
