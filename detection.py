from ultralytics import YOLO
from roboflow import Roboflow
from PIL import Image

food_list = ['된장찌개', '어묵볶음', '잔치국수', '제육볶음', '김치찜', '콩나물국', '콩나물무침', '쌀밥', '순두부찌개', '육개장']

# display image
def display_image(image_path, width=100):
    img = Image.open(image_path)

    img.show()

# detect food from image
def detection(image_path):
    # test image
    test_image = image_path

    display_image(test_image)

    # load model from roboflow
    rf = Roboflow(api_key="On22bsh1BDNtkVfYZhG9")
    project = rf.workspace("ybigta24thproject").project("what-the-food-9wdgr")

    model = project.version(4).model

    # detect food
    pred = model.predict(test_image, confidence=30, overlap=30).json()

    # make list of detected food
    detected_food = []
    for i in pred['predictions']:
        detected_food.append( food_list[i['class_id']] )

    return detected_food

if __name__ == "__main__":
    print("submit image file name")
    file_name = input()
    detected_food = detection(file_name)
    print(detected_food)