# 파이썬 OpenCV를 통한 도형검출

특정 이미지에서 점,선,삼각형,사각형 등의  각종 도형들을 검출하기 위해서 Python Open CV를 사용합니다. Open CV를 통해 이미지를 불러오고 외곽선을 검출하여 꼭지점을 구한 후, **꼭짓점 개수**를 통해 어떤 도형인지 식별합니다.

## Open CV 설치

: OpenCV 를 사용하기 위해서는 관련 모듈을 설치해야합니다.

- 설치

```bash
pip install opencv-python
```

- 설치 확인

```python
import cv2

print(cv2.__version__)

# 실행 결과 
4.6.0
```



### 스레시홀딩(Thresholding)

: 스레시홀딩은 바이너리 이미지를 만드는 가장 대표적인 방법입니다. 바이너리 이미지(binary image)란 검은색과 흰색만으로 표현한 이미지를 의미합니다. 스레시홀딩이란 여러 값을 어떤 임계점을 기준으로 두 가지 부류로 나누는 방법을 의미합니다.

[OpenCV - 8. 스레시홀딩(Thresholding), 오츠의 알고리즘(Otsu's Method)](https://bkshin.tistory.com/entry/OpenCV-8-%EC%8A%A4%EB%A0%88%EC%8B%9C%ED%99%80%EB%94%A9Thresholding)

이진화시킨 이미지에서 findContours함수를 사용하여 contour를 찾은 후, approxPolyDP 함수를 사용하여 다각형(polygon)을 검출합니다.

## 이미지 전처리

- 원본 이미지

![image](https://user-images.githubusercontent.com/86418674/206462395-72a97803-78a0-4309-a385-45ad33f4b979.png)


: 다음 테스트용 이미지를 저장하여 OpenCV를 위한 프로젝트 폴더에 넣습니다.

- 이미지 불러오기

```python
path = os.path.join('img','sample.jpg') # img 는 폴더명, sample.jpg는 테스트할 사진명
img_color = cv.imread(path, cv.IMREAD_COLOR)
```

OpenCV 는 **검은색 배경에 흰색 객체를 식별**하여 검출합니다. 따라서 이미지 색상을 반전하고 아래처럼 뿌옇거나 명암이 정확하지 않은 사진의 경우에는 스레시홀딩을 통해 도형을 정확히 검출할 수 있도록 최적화된 바이너리 이미지를 생성합니다. 


- 그레이 스케일로 변환

```python
img = cv2.imread(path)
img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
```

: 이미지를 불러오고 그레이 스케일로 변환합니다.

**[결과]**

![image](https://user-images.githubusercontent.com/86418674/206462446-ccb99cd3-4b77-4840-ace0-ec94ebb9da81.png)



- 이진화

```python
ret,img_binary = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY_INV|cv.THRESH_OTSU)
```

:  컨투어를 검출할 도형이 흰색영역이 되고 배경은 검은색이 되도록 색상을 반전합니다.

**[결과]**
![image](https://user-images.githubusercontent.com/86418674/206462494-9ac2da56-8d26-452e-b4e1-cb63db361f3f.png)


## 도형 외곽선 검출

```python
contours, hierarchy = cv.findContours(img_binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
```

: `findContours` 함수를 사용하여 바이너리 이미지에서 외곽선을 검출합니다. `cv.RETR_EXTERNAL` 옵션을 주어 외곽에 있는 컨투어만 검출하도록 합니다. `CHAIN_APPROX_SIMPLE` 옵션을 사용하여 검출되는 컨투어의 구성점 개수를 줄여줍니다. 예를들어 직선 부분이 있으면 양 끝점만 저장합니다.

<aside>
📌 **cv2.findContours(image, mode, method, contours=None, hierarchy=None, offset=None) -> contours, hierarchy**

- image: 입력 영상. non-zero 픽셀을 객체로 간주함.
- mode: 외곽선 검출 모드. cv2.RETR_로 시작하는 상수.
- method: 외곽선 근사화 방법. cv2.CHAIN_APPROX_로 시작하는 상수.
- contours: 검출된 외곽선 좌표. numpy.ndarray로 구성된 리스트. len(contours)=전체 외곽선 개수(N). contours[i].shape=(K, 1, 2). contours[i].dtype=numpy.int32.
- hierarchy: 외곽선 계층 정보. numpy.ndarray. shape=(1, N, 4). dtype=numpy.int32. hierarchy[0, i, 0] ~ hierarchy[0, i, 3]이 순서대로 next, prev, child, parent 외곽선 인덱스를 가리킴. 해당 외곽선이 없으면 -1.
- offset: 좌표 값 이동 옵셋. 기본값은 (0, 0).
</aside>

```python
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
```

: 검출된 컨투어를 직선으로 근사화 시킵니다. 이를 위해 우선 for문을 사용하여 컨투어리스트에서 컨투어를 하나씩 꺼냅니다. `approxPolyDP` 함수를 사용하여 컨투어를 직선으로 근사화하고, 직선으로 근사화된 컨투어를 입력이미지에 그려줍니다.


**[결과]**

: 도형 주변에 녹색선(컨투어)이 그려집니다.
![image](https://user-images.githubusercontent.com/86418674/206462722-eda202c7-5dc7-4667-bbe9-38c6da295482.png)

- 라벨링

```python
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
```

:  도형이 잘 구별되었는지 확인하기위해서 컨투어 영역내에 텍스트를 출력하는 setLabel 함수를 생성합니다. `cv.boundingRect` 를 통해 주어진 문자열 외곽을 둘러쌀 수 있는 박스의 너비와 높이를 계산하고 컨투어 외곽을 둘러싸는 박스의 정 중앙에 텍스트와 텍스트 박스를 출력합니다.


📌 **cv2.boundingRect**
: contour에 외접하는 똑바로 세워진 사각형을 얻기 위해 cv2.boundingRect() 함수를 이용합니다. cv2.boundingRect() 함수는 인자로 받은 contour에 외접하고 똑바로 세워진 직사각형의 좌상단 꼭짓점 좌표(x,y)와 가로 세로 폭을 리턴합니다. 

```python
x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
```



```python
for cont in contours:
    approx = cv2.approxPolyDP(cont,cv2.arcLength(cont,True)*0.02,True)
    vtc=len(approx)
```

: 검출된 외곽선들을 반복하면서 꼭짓점을 구합니다.

그러나 컨투어를 직선으로 근사화하여 얻은 직선의 개수만 가지고 도형을 판정시 문제가 발생합니다. 오목하게 들어간 도형과 내부에 구멍이 뚫린 도형을 사각형으로 인식합니다.

```python
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
        else:
            setLabel(img_color, str(size), cnt)
    else:
        setLabel(img_color, str(size), cnt)
```

이때, `isContourConvex` 함수를 사용하면 오목하게 들어간 경우를 제외시킬 수 있습니다.

아래 사진에서  오목하게 들어간 도형을 사각형에서 제외시킵니다.

**[결과]**
![image](https://user-images.githubusercontent.com/86418674/206462925-b8ebc8bd-dd88-4619-bbf4-1ae2240cdde4.png)


# 전체소스코드

 

```python
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

path = os.path.join('img','shapes.png')
img_color = cv.imread(path, cv.IMREAD_COLOR)

cv.imshow('result', img_color)
#cv.waitKey(0)

img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
cv.imshow('result', img_gray)
#cv.waitKey(0)

ret,img_binary = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY_INV|cv.THRESH_OTSU)
cv.imshow('result', img_binary)
#cv.waitKey(0)

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
        else:
            setLabel(img_color, str(size), cnt)
    else:
        setLabel(img_color, str(size), cnt)

cv.imshow('result', img_color)
cv.waitKey(0)
```

# 결과

![image](https://user-images.githubusercontent.com/86418674/206462820-de30f7ec-7e50-4104-9d03-9fd0f48d6100.png)
