from ultralytics import YOLO

class object_detection:

    def __init__(self):
        # Load a pretrained YOLOv8n model
        self._model = YOLO("yolov8n.pt")
        self._objects = []

    def detect(self, image):
        '''
            returns a list of recognized objects defined in dict of their   
            boundry box dimension and their name - 
            boundryBox = [center_x, center_y, w, h] 
        '''
        # Run inference on the source
        _results = self._model(image, save=False)  # list of Results _objects
        for obj in _results:
            _boxes = obj.boxes
            for box in _boxes:
                _box_dimensions = box.xywh
                _box_dimensions = _box_dimensions[0].int()

                _cls_id = box.cls  # Class ID of the detected object
                _obj_name = self._model.names[int(_cls_id)]  # Convert class ID to class name

                _object = {'boundry_box':_box_dimensions, 'name':_obj_name}
                self._objects.append(_object)
        return self._objects

    def _in_object(self, point, box):
        '''
            this point is inside the box or not
            point : x, y
            box: center_x, center_y, w, h
        '''
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
        
    def is_an_object(self, point):
        '''
            point is a list of x, y  
            ex: point = [510, 320]
        '''
        for obj in self._objects:
            _obj_boundry_box = obj['boundry_box']
            if self._in_object(point,_obj_boundry_box): ### point inside the object
                return obj
            else:
                return False



if __name__ == "__main__":
    objects = object_detection()

    # Define path to the image file
    source = "./detected_image.jpg"
    check_point = [592, 397]
    check_point2 = [10, 20]
    object_data = objects.detect(source)
    # print(object_data)
    print(objects.is_an_object(check_point2))
