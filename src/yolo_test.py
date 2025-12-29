from ultralytics import YOLO
import cv2

# Load YOLOv8 model (auto-downloads)
model = YOLO("yolov8n.pt")

# Load image
img = cv2.imread("data/images/test.png")

results = model(img)

# Draw results
annotated = results[0].plot()

cv2.imshow("YOLO Detection", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()
