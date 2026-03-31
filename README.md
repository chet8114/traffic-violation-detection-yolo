# 🚦 Traffic Violation Detection System

An **AI-powered Traffic Violation Detection System** built using **YOLOv8 and Streamlit**.
This application detects traffic rule violations from **images and videos** using deep learning.

## 🚨 Violations Detected

* ❌ **No Helmet Detection** – Detects riders without helmets using a **custom-trained YOLOv8 model**.
* 👥 **Triple Riding Detection** – Detects when more than **two persons ride on a motorcycle**.

The application provides an **interactive Streamlit interface** where users can upload traffic images or videos to check for violations.

---

# 🧠 Models Used

This project uses **two YOLO models**.

## 1️⃣ Custom Helmet Detection Model

A YOLOv8 model trained specifically to detect **riders without helmets**.

Download the trained model from Hugging Face:

https://huggingface.co/spaces/chethankarnati/helmet-detection-demo/blob/main/best.pt

After downloading, place the model inside:

```
runs/detect/train/weights/best.pt
```

---

## 2️⃣ YOLOv8 General Object Detection Model

Used for detecting:

* **Persons**
* **Motorcycles**

This model helps detect **triple riding violations**.

Model file:

```
yolov8n.pt
```

It will automatically download when running the code using Ultralytics.

---

# 📊 Model Performance

The **YOLOv8 helmet detection model** was trained and evaluated on a custom dataset.
Key evaluation metrics obtained during validation are shown below:

* **Precision**: 0.7970
* **Recall**: 0.8108
* **F1-Score**: 0.8038
* **mAP@0.5**: 0.8279
* **mAP@0.5:0.95**: 0.4762

The **F1-score** is calculated as:

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

These results indicate good detection capability for helmet violations under varying traffic conditions.

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
│   └──best.py
│
└── yolov8n.pt
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```
git clone https://github.com/YOUR_USERNAME/traffic_violation_detector.git
cd traffic_violation_detector
```

---

# 🐍 Create Virtual Environment

### Windows

```
python -m venv venv
```

---

# ▶️ Activate Virtual Environment

### PowerShell

```
venv\Scripts\activate
```

### Command Prompt

```
venv\Scripts\activate.bat
```

After activation, you should see:

```
(venv)
```

in your terminal.

---

# 📦 Install Dependencies

```
pip install streamlit ultralytics numpy
```

You may also generate a requirements file using:

```
pip freeze > requirements.txt
```

and install dependencies with:

```
pip install -r requirements.txt
```

---

# 🧠 Download Model

Download the trained helmet detection model from Hugging Face:

https://huggingface.co/spaces/chethankarnati/helmet-detection-demo/blob/main/best.pt

Place it inside:

```
runs/detect/train/weights/
```

Final path:

```
runs/detect/train/weights/best.pt
```

---

# ▶️ Run the Application

Start the Streamlit application:

```
streamlit run final.py
```

After running the command, the application will open automatically in your browser.

---

# 📷 Image Detection

1. Select **Image Mode**
2. Upload a traffic image
3. The system detects:

   * No Helmet riders
   * Triple Riding violations
4. Results are displayed with bounding boxes.

---

# 🎥 Video Detection

1. Select **Video Mode**
2. Upload a traffic video
3. The system processes video frames
4. If violations occur, the frame containing the violation is displayed.

The system also shows:

* Violation alerts
* Processing time
* Detected frames

---

# ⚙️ Detection Logic

## No Helmet Detection

A **custom YOLOv8 model** detects riders labeled as **Without Helmet**.

## Triple Riding Detection

1. YOLO detects **persons and motorcycles**.
2. The system checks for **bounding box overlap**.
3. If **more than two persons overlap with a motorcycle**, it is marked as **Triple Riding**.

---

# 🧰 Technologies Used

* Python
* Streamlit
* YOLOv8 (Ultralytics)
* NumPy

---

# 🚀 Future Improvements

* Number plate detection
* Real-time CCTV monitoring
* Automated traffic violation reporting
* Integration with smart traffic systems

---



