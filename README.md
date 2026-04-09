Nicee — deploying your app on Streamlit is a big upgrade for your project profile 🚀
Since now your project is **live**, your README should highlight the **Live Demo first** (this makes recruiters instantly interested).

Here’s your **updated professional GitHub README.md** with your Streamlit deployment added, structure improved, and small corrections fixed 👇

---

# 🚦 Traffic Violation Detection System

An **AI-powered Traffic Violation Detection System** built using **YOLOv8 and Streamlit** that detects traffic rule violations from **images and videos** using deep learning.

🔗 **Live Demo (Try the App Here):**
[https://traffic-violation-detection-yolo-chethan.streamlit.app/](https://traffic-violation-detection-yolo-chethan.streamlit.app/)

This application allows users to upload traffic images or videos and automatically detect violations through an interactive web interface.

---

# 🚨 Violations Detected

### ❌ No Helmet Detection

Detects riders without helmets using a **custom-trained YOLOv8 model**

### 👥 Triple Riding Detection

Detects when more than **two persons ride on a motorcycle**

---

# 🌐 Live Application Features

Users can:

✔ Upload traffic images
✔ Upload traffic videos
✔ Detect violations instantly
✔ View bounding box predictions
✔ Receive violation alerts
✔ See processed violation frames

No installation required — works directly in browser via Streamlit deployment.

---

# 🧠 Models Used

This project uses **two YOLO models**

---

## 1️⃣ Custom Helmet Detection Model

A YOLOv8 model trained specifically to detect:

* Riders **without helmets**

Download model from Hugging Face:

[https://huggingface.co/spaces/chethankarnati/helmet-detection-demo/blob/main/best.pt](https://huggingface.co/spaces/chethankarnati/helmet-detection-demo/blob/main/best.pt)

Place inside:

```
runs/detect/train/weights/best.pt
```

---

## 2️⃣ YOLOv8 General Object Detection Model

Used for detecting:

* Persons
* Motorcycles

This enables **triple riding violation detection**

Model file:

```
yolov8n.pt
```

It downloads automatically when running using Ultralytics.

---

# 📊 Model Performance

Helmet Detection Model Evaluation Metrics:

| Metric       | Score  |
| ------------ | ------ |
| Precision    | 0.7970 |
| Recall       | 0.8108 |
| F1 Score     | 0.8038 |
| mAP@0.5      | 0.8279 |
| mAP@0.5:0.95 | 0.4762 |

These results indicate strong detection performance under varied traffic conditions.

---

# 🗂 Project Structure

```
traffic_violation_detector
│
├── app.py
├── README.md
├── requirements.txt
│
├── models
│   └── best.pt
│
└── yolov8n.pt
```

---

# ⚙️ Installation (Run Locally)

## 1️⃣ Clone Repository

```
git clone https://github.com/YOUR_USERNAME/traffic_violation_detector.git
cd traffic_violation_detector
```

---

## 2️⃣ Create Virtual Environment

Windows:

```
python -m venv venv
```

---

## 3️⃣ Activate Environment

PowerShell:

```
venv\Scripts\activate
```

Command Prompt:

```
venv\Scripts\activate.bat
```

---

## 4️⃣ Install Dependencies

```
pip install -r requirements.txt
```

Or manually:

```
pip install streamlit ultralytics numpy opencv-python
```

---

## 5️⃣ Download Helmet Detection Model

Download:

[https://huggingface.co/spaces/chethankarnati/helmet-detection-demo/blob/main/best.pt](https://huggingface.co/spaces/chethankarnati/helmet-detection-demo/blob/main/best.pt)

Place inside:

```
runs/detect/train/weights/
```

Final path:

```
runs/detect/train/weights/best.pt
```

---

# ▶️ Run Application Locally

```
streamlit run app.py
```

Then open browser:

```
http://localhost:8501
```

---

# 📷 Image Detection Workflow

1️⃣ Select **Image Mode**
2️⃣ Upload traffic image
3️⃣ System detects:

* No helmet riders
* Triple riding violations

4️⃣ Results displayed with bounding boxes

---

# 🎥 Video Detection Workflow

1️⃣ Select **Video Mode**
2️⃣ Upload traffic video
3️⃣ Frames processed automatically
4️⃣ Violation frames highlighted

Displays:

* Violation alerts
* Detection output frames
* Processing feedback

---

# ⚙️ Detection Logic

## No Helmet Detection

Custom YOLOv8 model detects:

```
Without Helmet
```

label directly from trained dataset.

---

## Triple Riding Detection

Detection steps:

1. Detect persons and motorcycles using YOLOv8
2. Check bounding box overlap
3. If **more than two persons overlap with a motorcycle**
4. Mark as:

```
Triple Riding Violation
```

---

# 🧰 Technologies Used

* Python
* Streamlit
* YOLOv8 (Ultralytics)
* OpenCV
* NumPy

---

# 🚀 Future Improvements

Planned upgrades:

* Number plate detection
* Real-time CCTV integration
* Automatic challan generation system
* Smart traffic signal integration
* Cloud-based violation monitoring dashboard

---
