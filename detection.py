import json
from ultralytics import YOLO
from PIL import Image

weight_path = 'Object_detection\YOLO_weights\\best.pt'
food_list = ['된장찌개', '어묵볶음', '잔치국수', '제육볶음', '김치찜', '콩나물국', '콩나물무침', '쌀밥', '순두부찌개', '육개장']

def display_image(image_path, width=100):
    img = Image.open(image_path)

    img.show()

def detection(image_path):
    # test image
    test_image = image_path
    display_image(test_image)

    # load food
    model = YOLO(weight_path)

    # detect food
    pred = model.predict(test_image, conf = 0.3, verbose=False)
    names = model.names

    # make list of detected food
    detected_food = []
    for r in pred:
        for c in r.boxes.cls:
            detected_food.append(food_list[int(c)])
    
    return detected_food

if __name__ == "__main__":
    print("submit image file name")
    file_name = input()
    detected_food = detection(file_name)
    print("detected_food:", detected_food)