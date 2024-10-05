import cv2
import numpy as np
import math

PI = math.pi

# set parameter
img = cv2.imread('line2.jpg')
h, w, _ = img.shape
Thres = int((h+w)/4)

# sharping
imgCP = img.copy()
Y, Cr, Cb = cv2.split(cv2.cvtColor(imgCP, cv2.COLOR_BGR2YCrCb))
edges = cv2.Canny(Y, 100, 200)
edge_color = cv2.cvtColor(cv2.merge((edges, Cr, Cb)), cv2.COLOR_YCrCb2BGR)

# Detect lines
lines = cv2.HoughLinesP(edges, 1, np.pi/180, Thres, None, 20, 2)
imgLine = img.copy()

# get tiling angle 
angleXs, angleYs = [], []
for line in lines:
    x1, y1, x2, y2 = line[0]
    dx, dy = x1-x2, y1-y2
    if (dx < 0): dx, dy = -dx, -dy
    
    if (-PI/4 <= math.atan(dy/dx) <= PI/4): 
        angle = math.atan(dy/dx)
        angleXs.append(angle)
    else:
        angle = math.atan(dx/dy)
        angleYs.append(angle)
        
    print(angle*180/PI)
    cv2.line(imgLine, (x1,y1), (x2, y2), (0, 255, 0), 2)
        
angleX = sum(angleXs)/len(angleXs)
angleY = sum(angleYs)/len(angleYs)

# recover
cx, sx, cy, sy = math.cos(angleX), math.sin(angleX), math.cos(angleY), math.sin(angleY)
imgMod = np.zeros((h, w, 3), np.uint8)
for x in range(w):
    for y in range(h):
        xx = int((x*cy-y*sy)/(cx*cy-sx*sy))
        yy = int((x*sx-y*cx)/(sx*sy-cx*cy))
        
        if (not 0<=xx<w or not 0<=yy<h): continue

        imgMod[yy, xx, :] = img[y, x, :]
    
merged = cv2.resize(np.hstack((img,imgLine, imgMod)), (w*3*5, h*5))

cv2.imshow('Probability hough line', merged)
cv2.waitKey()
cv2.imwrite('test.png', merged)
cv2.destroyAllWindows()
