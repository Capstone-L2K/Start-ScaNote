# Start-ScaNote

## 1단계 : [Image 전처리](Image_전처리.ipynb)

![01 이미지 전처리](https://user-images.githubusercontent.com/84276596/206180559-65e24e71-04a5-446f-93af-df7beb016018.png)

- Tesseract를 이용한 Outline detection 및 영역 Grouping
    - 예시 이미지를 통해 outline detection 및 영역 grouping
- 먼저 Tesseract를 이용해서 이미지 전처리를 진행할 수 있다. 사용자가 서비스를 통해 이미지를 찍으면, 원본 이미지를 불러와서 해당 이미지의 gray, blurred, edged 이미지를 만들어낸다. 이 과정을 통해서 contours를 추출할 수 있다. 이 중 가장 큰 contours는 edge가 되고, 이 edge를 기준으로 이미지를 crop할 수 있다.
- 또한 crop된 이미지 내에서 적절한 종횡비를 이용하여 연관이 있는 내용 간에 적절하게 grouping 할 수 있다. 마지막 이미지에서 빨간색 라인으로 grouping 된 모습을 볼 수 있다.
<br>
<br>
<br>

## 2단계 : [광 문자 인식(OCR)]()

![02 OCR](https://user-images.githubusercontent.com/84276596/206180581-9788d6d1-0db3-4040-bef7-315629d7dbc3.png)

- Google Cloud Platform의 Cloud Vision API 중 광 문자 인식(OCR)을 사용하여 유저의 종이 문서, 판서에서 텍스트를 검출하여 변환한다. 각 텍스트 경계 상자의 위치 좌표도 얻을 수 있다.
<br>
<br>
<br>

## 3단계 : [Phthon OpenCV를 이용한 개체 인식 및 도형 검출]()

![03 OpenCV](https://user-images.githubusercontent.com/84276596/206180589-5fb7a242-e7cb-4146-8321-905bef913098.png)

- 특정 이미지에서 점,선,삼각형,사각형 등의  각종 도형들을 검출하기 위해서 Python Open CV를 사용한다. Open CV를 통해 이미지를 불러오고 외곽선을 검출하여 꼭지점을 구한 후, 꼭짓점 개수를 통해 어떤 도형인지 식별한다.

