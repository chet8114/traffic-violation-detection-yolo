import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import numpy as np
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Traffic Violation Detector", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main-title {
    font-size: 42px;
    font-weight: bold;
    color: #FFD700;
    text-align: center;
}

.sub-title {
    font-size: 20px;
    color: #ffffff;
    text-align: center;
    margin-bottom: 30px;
}

.section-card {
    background-color: rgba(255, 255, 255, 0.08);
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
}

.quote-box {
    background-color: rgba(255, 215, 0, 0.15);
    padding: 20px;
    border-radius: 12px;
    margin-top: 40px;
    text-align: center;
    font-size: 18px;
    color: #ffffff;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🚦 Traffic Violation Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI Powered Monitoring for Safer Roads</div>', unsafe_allow_html=True)

# ---------------- LOAD MODELS ----------------
@st.cache_resource
def load_models():
    helmet = YOLO("runs/detect/train/weights/best.pt")
    general = YOLO("yolov8n.pt")
    return helmet, general

helmet_model, general_model = load_models()

# ---------------- MODE SELECTION ----------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
mode = st.radio("📌 Select Input Type", ["Image", "Video"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# ================= IMAGE SECTION =====================
# =====================================================

if mode == "Image":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📷 Upload Traffic Image", type=["jpg", "jpeg", "png"])
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:

        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        violation_messages = []
        no_helmet_detected = False
        triple_riding_detected = False

        helmet_results = helmet_model(frame, conf=0.6, verbose=False)

        for box in helmet_results[0].boxes:
            class_id = int(box.cls[0])
            class_name = helmet_results[0].names[class_id]
            if class_name == "Without Helmet":
                no_helmet_detected = True

        general_results = general_model(frame, conf=0.4, verbose=False)

        persons = []
        motorcycles = []

        for box in general_results[0].boxes:
            class_id = int(box.cls[0])
            class_name = general_results[0].names[class_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if class_name == "person":
                persons.append((x1, y1, x2, y2))
            if class_name in ["motorcycle", "motorbike"]:
                motorcycles.append((x1, y1, x2, y2))

        for bike in motorcycles:
            bx1, by1, bx2, by2 = bike
            count = 0
            for person in persons:
                px1, py1, px2, py2 = person
                if px1 < bx2 and px2 > bx1 and py1 < by2 and py2 > by1:
                    count += 1
            if count > 2:
                triple_riding_detected = True
                break

        if no_helmet_detected:
            violation_messages.append("❌ No Helmet Detected")
        if triple_riding_detected:
            violation_messages.append("👥 Triple Riding Detected")

        if violation_messages:
            st.error("🚨 Traffic Violation Detected!")
            for msg in violation_messages:
                st.write(msg)
            annotated_frame = helmet_results[0].plot()
            st.image(annotated_frame, channels="BGR")
        else:
            st.success("✅ No Violation Detected")
            st.image(frame, channels="BGR")


# =====================================================
# ================= VIDEO SECTION =====================
# =====================================================

if mode == "Video":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("🎥 Upload Traffic Video", type=["mp4", "avi", "mov"])
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:

        temp_video = tempfile.NamedTemporaryFile(delete=False)
        temp_video.write(uploaded_file.read())

        cap = cv2.VideoCapture(temp_video.name)

        helmet_saved = False
        triple_saved = False
        helmet_image = None
        triple_image = None

        frame_id = 0
        frame_skip = 5
        start_time = time.time()

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar = st.progress(0)

        with st.spinner("🔍 Processing video..."):

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_id += 1
                progress_bar.progress(min(frame_id / total_frames, 1.0))

                if frame_id % frame_skip != 0:
                    continue

                frame = cv2.resize(frame, (640, 480))

                if not helmet_saved:
                    helmet_results = helmet_model(frame, conf=0.6, verbose=False)
                    for box in helmet_results[0].boxes:
                        class_id = int(box.cls[0])
                        class_name = helmet_results[0].names[class_id]
                        if class_name == "Without Helmet":
                            helmet_saved = True
                            helmet_image = helmet_results[0].plot()
                            break

                if not triple_saved:
                    general_results = general_model(frame, conf=0.4, verbose=False)

                    persons = []
                    motorcycles = []

                    for box in general_results[0].boxes:
                        class_id = int(box.cls[0])
                        class_name = general_results[0].names[class_id]
                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        if class_name == "person":
                            persons.append((x1, y1, x2, y2))
                        if class_name in ["motorcycle", "motorbike"]:
                            motorcycles.append((x1, y1, x2, y2))

                    for bike in motorcycles:
                        bx1, by1, bx2, by2 = bike
                        count = 0
                        for person in persons:
                            px1, py1, px2, py2 = person
                            if px1 < bx2 and px2 > bx1 and py1 < by2 and py2 > by1:
                                count += 1
                        if count > 2:
                            triple_saved = True
                            triple_image = general_results[0].plot()
                            break

                if helmet_saved and triple_saved:
                    break

        cap.release()
        end_time = time.time()

        st.success("✅ Processing Completed!")
        st.write(f"⏱ Processing Time: {round(end_time - start_time, 2)} seconds")

        if helmet_image is not None:
            st.subheader("❌ No Helmet Violation")
            st.image(helmet_image, channels="BGR")

        if triple_image is not None:
            st.subheader("👥 Triple Riding Violation")
            st.image(triple_image, channels="BGR")

        if helmet_image is None and triple_image is None:
            st.warning("No violations detected in this video.")


# ---------------- QUOTATION SECTION ----------------
