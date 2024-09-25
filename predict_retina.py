from ultralytics import YOLO
# from ultralytics.yolo.v8.detect.predict import DetectionPredictor

model = YOLO("/root/Work/yolov8/yolov8_medical/retina_seg.pt")
# model = YOLO("/root/Work/yolov8/yolov8_medical/model/retina_detect_1221.pt")
model.info()

import glob
from IPython.display import Image, display

# for image_path in glob.glob(f'/root/Work/yolov8/yolov8_medical/DDR-Set-2/DDR-Set-2/test/images/*jpg'):
#       results = model.predict(source=image_path,project="/root/Work/yolov8/yolov8_medical/result/segment/retina3",name="retina",save=True)
#       print("\n")
for image_path in glob.glob(f'/root/Work/yolov8/yolov8_medical/HE_dataset/*jpg'):
      results = model.predict(source=image_path,project="/root/Work/yolov8/yolov8_medical/result/segment/20240108_HE",name="retina",save=True)
      print("\n")