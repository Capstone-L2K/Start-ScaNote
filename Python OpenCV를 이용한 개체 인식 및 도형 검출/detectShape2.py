import cv2 as cv
import os


# 컨투어 영역내에 텍스트 출력
def setLabel(image, str, contour):
    (text_width, text_height), baseline = cv.getTextSize(str, cv.FONT_HERSHEY_SIMPLEX, 0.7, 1)
    
    # 주어진 문자열 외곽을 둘러쌀 수 있는 박스의 너비와 높이를 계산
    x,y,width,height = cv.boundingRect(contour)
    
    # 컨투어 외곽을 둘러싸는 박스의 정 중앙에 텍스트와 텍스트 박스를 출력합니다.
    pt_x = x+int((width-text_width)/2)
    pt_y = y+int((height + text_height)/2)
    cv.rectangle(image, (pt_x, pt_y+baseline), (pt_x+text_width, pt_y-text_height), (200,200,200), cv.FILLED)
    cv.putText(image, str, (pt_x, pt_y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, 8)




path = os.path.join('img','test.png')
img_color = cv.imread(path, cv.IMREAD_COLOR)


cv.imshow('result', img_color)
cv.waitKey(0)

img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
cv.imshow('result', img_gray)
cv.waitKey(0)

ret,img_binary = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY_INV|cv.THRESH_OTSU)
cv.imshow('result', img_binary)
cv.waitKey(0)

contours, hierarchy = cv.findContours(img_binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    size = len(cnt)
    print(size)

    epsilon = 0.005 * cv.arcLength(cnt, True)
    approx = cv.approxPolyDP(cnt, epsilon, True) # 컨투어를 직선으로 근사화

    size = len(approx) #근사화 시킨 후 컨투어를 구성하는 성분의 개수
   
   # 직선으로 근사화된 컨투어를 입력 이미지에 그린다.
    cv.line(img_color, tuple(approx[0][0]), tuple(approx[size-1][0]), (0, 255, 0), 3)
    for k in range(size-1):
        cv.line(img_color, tuple(approx[k][0]), tuple(approx[k+1][0]), (0, 255, 0), 3)


    if cv.isContourConvex(approx): # 근사화된 직선의 개수를 활용하여 컨투어 내부의 도형이름을 출력합니다.
        if size ==2:
            setLabel(img_color, "line", cnt)
        elif size == 3:
            setLabel(img_color, "triangle", cnt)
        elif size == 4:
            setLabel(img_color, "rectangle", cnt)
        elif size == 5:
            setLabel(img_color, "pentagon", cnt)
        elif size == 6:
            setLabel(img_color, "hexagon", cnt)
        elif size == 8:
            setLabel(img_color, "octagon", cnt)
        elif size == 10:
            setLabel(img_color, "decagon", cnt)
        #else:
            #setLabel(img_color, str(size), cnt)
    #else:
        #setLabel(img_color, str(size), cnt)

cv.imshow('result', img_color)
cv.waitKey(0)