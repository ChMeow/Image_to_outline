import numpy as np
import cv2

def img_to_outline(video_frame):
    # Graycsale, Blur
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 3)

    # Sobel Edge Detection
    #sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
    #sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) 
    #sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) 

    # Canny Edge Detection
    sigma_multiplier = 2
    sigma = np.std(img_blur)
    mean = np.mean(img_blur)
    lower = int(max(0, (mean - sigma_multiplier*sigma)))
    upper = int(min(255, (mean + sigma_multiplier*sigma)))
    edges = cv2.Canny(img_blur, lower, upper)

    #Morphology, Dilation, and Erosion
    #morph_open = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)
    morph_close = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    dilation = cv2.dilate(morph_close,kernel,iterations = 2)
    erosion = cv2.erode(dilation,kernel,iterations = 2)

    results = erosion
    return results


kernel_size = 2
kernel = np.ones((kernel_size,kernel_size),np.uint8)
#img = cv2.imread("C:\\wallpaper\\25.jpg")
cap = cv2.VideoCapture("C:\\wallpaper\\1.mp4")
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
out = cv2.VideoWriter('output.mp4', fourcc, fps, (int(width),int(height)), False)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    converted_frame = img_to_outline(frame)
    out.write(converted_frame)
    cv2.imshow('frame', converted_frame)
    if cv2.waitKey(1) == ord('q'):
        break
 
cap.release()
out.release()
cv2.destroyAllWindows()
