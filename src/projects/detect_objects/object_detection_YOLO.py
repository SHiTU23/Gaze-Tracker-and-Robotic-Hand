from ultralytics import YOLO
import cv2
import numpy as np

def in_object(point, box):
    ### this point is inside the box or not
    ### point : x, y
    ### box: x,y,w,h
    point_x, point_y = point
    box_x, box_y, box_w, box_h = box
    box_w =int(box_w/2)
    box_h = int(box_h/2)
    toleranse = 5 
    if ((point_x > box_x-box_w-toleranse and point_x < box_x+box_w+toleranse) and
         (point_y > box_y-box_h-toleranse and point_y < box_y+box_h+toleranse)):
        return True
    else:
        return False
    
# Load a pretrained YOLOv8n model
model = YOLO("yolov8n.pt")

# Define path to the image file
source = "./detected_image.jpg"
img = cv2.imread(source)
img_h, img_w, channels = img.shape
print("image w and h : ", img_w, img_h)

# Run inference on the source
results = model(source, save=True)  # list of Results objects

point_original_dimensions = [1280, 720]
check_point = [592, 397]
x = int(np.interp(check_point[0], [0, point_original_dimensions[0]], [0, img_w]) )
y =int(abs(img_h - (np.interp(check_point[1], [0,point_original_dimensions[1]], [0, img_h]))))
print(f"mapped_x: {x}, y:{y}")

# View results
for r in results:
    # print("r:", r.id)
    # print(r.boxes.xywh)  # print the Boxes object containing the detection bounding boxes
    boxes = r.boxes
    for box in boxes:
        box_dimensions = box.xywh
        box_dimensions = box_dimensions[0].int()
        
        print("box_dimensions:", box_dimensions)
        if in_object(check_point,box_dimensions):
            cls_id = box.cls  # Class ID of the detected object
            cls_name = model.names[int(cls_id)]  # Convert class ID to class name
            print(f"Detected object: {cls_name}")
