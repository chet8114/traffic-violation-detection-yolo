# from ultralytics import YOLO
# import cv2

# # ==============================
# # Load YOLO model
# # ==============================
# model = YOLO("yolov8n.pt")

# # ==============================
# # Load input image
# # ==============================
# img = cv2.imread("data/images/test.png")

# if img is None:
#     print("❌ Image not found")
#     exit()

# # ==============================
# # Run YOLO detection
# # ==============================
# results = model(img)[0]

# # ==============================
# # Initialize counters
# # ==============================
# persons = 0
# bikes = 0
# helmets = 0
# traffic_lights = 0

# # ==============================
# # Read detections
# # ==============================
# for box in results.boxes:
#     cls_id = int(box.cls[0])
#     label = model.names[cls_id]

#     if label == "person":
#         persons += 1

#     elif label in ["motorcycle", "bike"]:
#         bikes += 1

#     elif label == "helmet":
#         helmets += 1

#     elif label == "traffic light":
#         traffic_lights += 1

# # ==============================
# # Print raw counts
# # ==============================
# print("Persons detected:", persons)
# print("Bikes detected:", bikes)
# print("Helmets detected:", helmets)
# print("Traffic lights detected:", traffic_lights)

# print("\n====== VIOLATION CHECK ======\n")

# # ==============================
# # 🚨 RULE 1: Triple Riding
# # ==============================
# if bikes > 0:
#     if persons > bikes * 2:
#         print("🚨 Triple Riding Violation Detected")
#     else:
#         print("✅ No Triple Riding Violation")
# else:
#     print("ℹ️ No bikes detected")

# # ==============================
# # 🚨 RULE 2: No Helmet
# # ==============================
# if bikes > 0 and persons > 0:
#     if helmets < persons:
#         print("🚨 No Helmet Violation Detected")
#     else:
#         print("✅ Helmet Rule Followed")

# # ==============================
# # 🚦 RULE 3: Red Light (Placeholder)
# # ==============================
# # NOTE:
# # Actual red-light violation needs:
# # - traffic signal color detection
# # - vehicle position vs stop line
# # We will implement this next

# if traffic_lights > 0:
#     print("ℹ️ Traffic light detected (logic coming next)")
# else:
#     print("ℹ️ No traffic light detected")

# print("\n====== END ======")
from ultralytics import YOLO
import cv2

# ==============================
# Load YOLO model
# ==============================
model = YOLO("yolov8n.pt")

# ==============================
# Load image
# ==============================
img = cv2.imread("data/images/test1.jpeg")

if img is None:
    print("❌ Image not found")
    exit()

# ==============================
# Run detection
# ==============================
results = model(img)[0]

# ==============================
# Initialize counters
# ==============================
persons = 0
bikes = 0
helmets = 0
traffic_lights = 0

# ==============================
# Read detections
# ==============================
for box in results.boxes:
    cls_id = int(box.cls[0])
    label = model.names[cls_id]

    if label == "person":
        persons += 1

    elif label in ["motorcycle", "bike"]:
        bikes += 1

    elif label == "helmet":
        helmets += 1

    elif label == "traffic light":
        traffic_lights += 1

# ==============================
# Print counts
# ==============================
print("Persons detected:", persons)
print("Bikes detected:", bikes)
print("Helmets detected:", helmets)
print("Traffic lights detected:", traffic_lights)

print("\n====== VIOLATION CHECK ======\n")

# ==============================
# 🚨 RULE 1: Triple Riding
# ==============================
if bikes > 0:
    if persons > bikes * 2:
        print("🚨 Triple Riding Violation Detected")
    else:
        print("✅ No Triple Riding Violation")
else:
    print("ℹ️ No bikes detected")

# ==============================
# 🚨 RULE 2: No Helmet
# ==============================
if bikes > 0 and persons > 0:
    if helmets < persons:
        print("🚨 No Helmet Violation Detected")
    else:
        print("✅ Helmet Rule Followed")

# ==============================
# 🚦 RULE 3: Red Light Violation
# ==============================

# ==============================
# 🚦 RULE 3: Red Light Violation (Cars + Bikes)
# ==============================

# Virtual stop line (70% of image height)
img_height = img.shape[0]
stop_line_y = int(img_height * 0.7)

red_light = traffic_lights > 0
red_light_violation = False

vehicle_classes = ["car", "motorcycle", "truck", "bus"]

if red_light:
    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]

        if label in vehicle_classes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # If vehicle crosses stop line
            if y2 > stop_line_y:
                red_light_violation = True
                break

    if red_light_violation:
        print("🚨 Red Light Violation Detected (Vehicle crossed stop line)")
    else:
        print("✅ Red Light Rule Followed (All vehicles stopped)")
else:
    print("ℹ️ Red light logic skipped")

