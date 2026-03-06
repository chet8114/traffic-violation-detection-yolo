import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import numpy as np
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Traffic Violation Detector", layout="wide", page_icon="🚦")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Exo+2:wght@300;400;500;600&family=Share+Tech+Mono&display=swap');

html, body, [data-testid="stAppViewContainer"] { background: #050a0f; }

[data-testid="stSidebar"] { display: none; }

.header-wrap { text-align:center; padding:50px 0 10px; }

.badge-line {
font-family:'Share Tech Mono', monospace;
font-size:11px;
letter-spacing:6px;
color:#00c87a;
text-transform:uppercase;
}

.main-title {
font-family:'Rajdhani', sans-serif;
font-size:58px;
font-weight:700;
letter-spacing:4px;
text-transform:uppercase;
background:linear-gradient(90deg,#00c87a,#00e5ff,#00c87a);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.sub-title {
font-family:'Exo 2', sans-serif;
font-size:15px;
color:rgba(255,255,255,0.45);
letter-spacing:5px;
text-transform:uppercase;
}

.divider {
height:1px;
background:linear-gradient(90deg,transparent,#00c87a,transparent);
margin:30px auto;
max-width:600px;
}

.violation-banner {
background:linear-gradient(135deg,rgba(255,45,85,0.12),rgba(255,100,0,0.08));
border:1px solid rgba(255,45,85,0.4);
border-radius:12px;
padding:18px 24px;
margin:16px 0;
font-family:'Rajdhani', sans-serif;
font-size:22px;
font-weight:700;
letter-spacing:2px;
color:#ff4d6d;
}

.safe-banner {
background:linear-gradient(135deg,rgba(0,200,122,0.12),rgba(0,229,255,0.06));
border:1px solid rgba(0,200,122,0.35);
border-radius:12px;
padding:18px 24px;
margin:16px 0;
font-family:'Rajdhani', sans-serif;
font-size:22px;
font-weight:700;
letter-spacing:2px;
color:#00c87a;
}

.footer-text {
font-family:'Share Tech Mono', monospace;
font-size:11px;
color:rgba(255,255,255,0.2);
text-align:center;
letter-spacing:3px;
margin-top:50px;
padding-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header-wrap">
<div class="badge-line">⬡ neural surveillance system v2.0 ⬡</div>
<div class="main-title">Traffic Violation<br>Detection</div>
<div class="sub-title">AI-Powered Road Safety Intelligence</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ---------------- LOAD MODELS ----------------
@st.cache_resource
def load_models():
    helmet = YOLO("runs/detect/train/weights/best.pt")
    general = YOLO("yolov8n.pt")
    return helmet, general

helmet_model, general_model = load_models()

# ---------------- MODE SELECTION ----------------
mode = st.radio("📌 SELECT INPUT MODE", ["Image", "Video"], horizontal=True)

# ================= IMAGE SECTION =================
if mode == "Image":

    uploaded_file = st.file_uploader("📷 UPLOAD TRAFFIC IMAGE", type=["jpg","jpeg","png"])

    if uploaded_file is not None:

        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        violation_messages=[]
        no_helmet=False
        triple=False

        helmet_results = helmet_model(frame,conf=0.6,verbose=False)

        for box in helmet_results[0].boxes:
            cls=int(box.cls[0])
            name=helmet_results[0].names[cls]
            if name=="Without Helmet":
                no_helmet=True

        general_results = general_model(frame,conf=0.4,verbose=False)

        persons=[]
        bikes=[]

        for box in general_results[0].boxes:
            cls=int(box.cls[0])
            name=general_results[0].names[cls]
            x1,y1,x2,y2=map(int,box.xyxy[0])

            if name=="person":
                persons.append((x1,y1,x2,y2))

            if name=="motorcycle":
                bikes.append((x1,y1,x2,y2))

        for bike in bikes:
            bx1,by1,bx2,by2=bike
            count=0
            for p in persons:
                px1,py1,px2,py2=p
                cx=(px1+px2)//2
                cy=(py1+py2)//2
                if bx1<cx<bx2 and by1<cy<by2:
                    count+=1
            if count>2:
                triple=True

        if no_helmet:
            violation_messages.append("❌ No Helmet Detected")
        if triple:
            violation_messages.append("👥 Triple Riding Detected")

        if violation_messages:
            st.markdown(f'<div class="violation-banner">🚨 {" · ".join(violation_messages)}</div>',unsafe_allow_html=True)
            st.image(helmet_results[0].plot(),channels="BGR",use_container_width=True)

        else:
            st.markdown('<div class="safe-banner">✅ No Violation Detected</div>',unsafe_allow_html=True)
            st.image(frame,channels="BGR",use_container_width=True)

# ================= VIDEO SECTION =================
if mode == "Video":

    uploaded_file = st.file_uploader("🎥 UPLOAD TRAFFIC VIDEO", type=["mp4","avi","mov"])

    if uploaded_file:

        temp=tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())

        cap=cv2.VideoCapture(temp.name)

        helmet_saved=False
        triple_saved=False
        helmet_image=None
        triple_image=None

        frame_id=0
        frame_skip=2
        start=time.time()

        total_frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        progress=st.progress(0)

        while True:

            ret,frame=cap.read()
            if not ret:
                break

            frame_id+=1

            if total_frames>0:
                progress.progress(min(frame_id/total_frames,1.0))

            if frame_id%frame_skip!=0:
                continue

            frame=cv2.resize(frame,(640,480))

            # Helmet detection
            if not helmet_saved:
                r=helmet_model(frame,conf=0.5,verbose=False)
                for b in r[0].boxes:
                    name=r[0].names[int(b.cls[0])]
                    if name=="Without Helmet":
                        helmet_saved=True
                        helmet_image=r[0].plot()

            # Triple riding detection
            if not triple_saved:

                r=general_model(frame,conf=0.35,verbose=False)

                persons=[]
                bikes=[]

                for b in r[0].boxes:

                    name=r[0].names[int(b.cls[0])]
                    x1,y1,x2,y2=map(int,b.xyxy[0])

                    if name=="person":
                        persons.append((x1,y1,x2,y2))

                    if name=="motorcycle":
                        bikes.append((x1,y1,x2,y2))

                for bike in bikes:

                    bx1,by1,bx2,by2=bike
                    count=0

                    for p in persons:

                        px1,py1,px2,py2=p
                        cx=(px1+px2)//2
                        cy=(py1+py2)//2

                        if bx1<cx<bx2 and by1<cy<by2:
                            count+=1

                    if count>2:
                        triple_saved=True
                        triple_image=r[0].plot()

            if helmet_saved and triple_saved:
                break

        cap.release()

        end=time.time()
        t=round(end-start,2)

        st.markdown(f"""
        <div class="safe-banner">
        ✅ Processing Complete · ⏱ {t}s · 📽 {frame_id} frames
        </div>
        """,unsafe_allow_html=True)

        # -------- NEW DISPLAY LOGIC --------

        if triple_image is not None and helmet_image is not None:

            st.markdown('<div class="violation-banner">🚨 Triple Riding Violation Detected</div>',unsafe_allow_html=True)
            st.image(triple_image,channels="BGR",use_container_width=True)

            st.markdown('<div class="violation-banner">❌ No Helmet Violation Detected</div>',unsafe_allow_html=True)

        elif triple_image is not None:

            st.markdown('<div class="violation-banner">🚨 Triple Riding Violation Detected</div>',unsafe_allow_html=True)
            st.image(triple_image,channels="BGR",use_container_width=True)

        elif helmet_image is not None:

            st.markdown('<div class="violation-banner">❌ No Helmet Violation Detected</div>',unsafe_allow_html=True)
            st.image(helmet_image,channels="BGR",use_container_width=True)

        else:

            st.markdown('<div class="safe-banner">✅ No Violations Detected in This Video</div>',unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown('<div class="footer-text">⬡ TRAFFIC VIOLATION DETECTION SYSTEM · AI POWERED · ROAD SAFETY MODULE ⬡</div>',unsafe_allow_html=True)