# import streamlit as st
# from ultralytics import YOLO
# import cv2
# import tempfile
# import numpy as np
# import time

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(page_title="Traffic Violation Detector", layout="wide", page_icon="🚦")

# # ---------------- CUSTOM CSS ----------------
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Exo+2:wght@300;400;500;600&family=Share+Tech+Mono&display=swap');

# html, body, [data-testid="stAppViewContainer"] {
#     background: #050a0f;
# }

# [data-testid="stAppViewContainer"] {
#     background:
#         radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0, 200, 120, 0.12) 0%, transparent 60%),
#         radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0, 120, 255, 0.08) 0%, transparent 50%),
#         #050a0f;
# }

# [data-testid="stSidebar"] { display: none; }

# /* Scanline overlay */
# [data-testid="stAppViewContainer"]::before {
#     content: '';
#     position: fixed;
#     top: 0; left: 0; right: 0; bottom: 0;
#     background: repeating-linear-gradient(
#         0deg,
#         transparent,
#         transparent 2px,
#         rgba(0,0,0,0.03) 2px,
#         rgba(0,0,0,0.03) 4px
#     );
#     pointer-events: none;
#     z-index: 0;
# }

# .header-wrap {
#     text-align: center;
#     padding: 50px 0 10px;
#     position: relative;
# }

# .badge-line {
#     font-family: 'Share Tech Mono', monospace;
#     font-size: 11px;
#     letter-spacing: 6px;
#     color: #00c87a;
#     text-transform: uppercase;
#     margin-bottom: 12px;
# }

# .main-title {
#     font-family: 'Rajdhani', sans-serif;
#     font-size: 58px;
#     font-weight: 700;
#     letter-spacing: 4px;
#     text-transform: uppercase;
#     background: linear-gradient(90deg, #00c87a, #00e5ff, #00c87a);
#     background-size: 200% auto;
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     animation: shimmer 4s linear infinite;
#     line-height: 1.1;
#     margin: 0;
# }

# @keyframes shimmer {
#     0% { background-position: 0% center; }
#     100% { background-position: 200% center; }
# }

# .sub-title {
#     font-family: 'Exo 2', sans-serif;
#     font-size: 15px;
#     font-weight: 300;
#     color: rgba(255,255,255,0.45);
#     letter-spacing: 5px;
#     text-transform: uppercase;
#     margin-top: 10px;
# }

# .divider {
#     height: 1px;
#     background: linear-gradient(90deg, transparent, #00c87a, transparent);
#     margin: 30px auto;
#     max-width: 600px;
# }

# /* Cards — target Streamlit widget blocks directly */
# div[data-testid="stRadio"],
# div[data-testid="stFileUploader"] {
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(0, 200, 122, 0.22);
#     border-radius: 14px;
#     padding: 28px 32px 28px 36px !important;
#     margin-bottom: 22px;
#     box-shadow: 0 0 30px rgba(0, 200, 122, 0.05), inset 0 1px 0 rgba(255,255,255,0.04);
#     position: relative;
# }

# div[data-testid="stRadio"]::before,
# div[data-testid="stFileUploader"]::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 0;
#     width: 4px; height: 100%;
#     background: linear-gradient(180deg, #00c87a, #00e5ff);
#     border-radius: 14px 0 0 14px;
# }

# /* Legacy class kept for other uses */
# .section-card {
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(0, 200, 122, 0.18);
#     border-radius: 12px;
#     padding: 28px 30px;
#     margin-bottom: 22px;
# }

# /* Violation banner */
# .violation-banner {
#     background: linear-gradient(135deg, rgba(255,45,85,0.12), rgba(255,100,0,0.08));
#     border: 1px solid rgba(255, 45, 85, 0.4);
#     border-radius: 12px;
#     padding: 18px 24px;
#     margin: 16px 0;
#     font-family: 'Rajdhani', sans-serif;
#     font-size: 22px;
#     font-weight: 700;
#     letter-spacing: 2px;
#     color: #ff4d6d;
#     text-transform: uppercase;
#     animation: pulse-red 2s ease-in-out infinite;
# }

# @keyframes pulse-red {
#     0%, 100% { box-shadow: 0 0 0 0 rgba(255,45,85,0); }
#     50% { box-shadow: 0 0 20px 2px rgba(255,45,85,0.2); }
# }

# .safe-banner {
#     background: linear-gradient(135deg, rgba(0,200,122,0.12), rgba(0,229,255,0.06));
#     border: 1px solid rgba(0, 200, 122, 0.35);
#     border-radius: 12px;
#     padding: 18px 24px;
#     margin: 16px 0;
#     font-family: 'Rajdhani', sans-serif;
#     font-size: 22px;
#     font-weight: 700;
#     letter-spacing: 2px;
#     color: #00c87a;
#     text-transform: uppercase;
# }

# .violation-label {
#     font-family: 'Rajdhani', sans-serif;
#     font-size: 14px;
#     font-weight: 600;
#     letter-spacing: 4px;
#     text-transform: uppercase;
#     color: #00e5ff;
#     margin: 24px 0 10px;
#     border-bottom: 1px solid rgba(0,229,255,0.2);
#     padding-bottom: 6px;
# }

# .stat-chip {
#     display: inline-block;
#     background: rgba(0,229,255,0.08);
#     border: 1px solid rgba(0,229,255,0.25);
#     border-radius: 20px;
#     padding: 4px 14px;
#     font-family: 'Share Tech Mono', monospace;
#     font-size: 13px;
#     color: #00e5ff;
#     margin: 4px;
# }

# .footer-text {
#     font-family: 'Share Tech Mono', monospace;
#     font-size: 11px;
#     color: rgba(255,255,255,0.2);
#     text-align: center;
#     letter-spacing: 3px;
#     margin-top: 50px;
#     padding-bottom: 20px;
# }

# /* Radio — big label + big options */
# div[data-testid="stRadio"] > label,
# div[data-testid="stRadio"] p {
#     font-family: 'Rajdhani', sans-serif !important;
#     font-size: 20px !important;
#     font-weight: 600 !important;
#     letter-spacing: 3px !important;
#     text-transform: uppercase !important;
#     color: #00e5ff !important;
#     margin-bottom: 18px !important;
# }

# div[data-testid="stRadio"] > div {
#     gap: 30px;
#     margin-top: 6px;
# }

# div[data-testid="stRadio"] label span {
#     font-family: 'Exo 2', sans-serif !important;
#     font-size: 18px !important;
#     font-weight: 500 !important;
#     color: rgba(255,255,255,0.88) !important;
#     letter-spacing: 1px !important;
# }

# div[data-testid="stRadio"] input[type="radio"] {
#     accent-color: #00c87a;
#     width: 18px;
#     height: 18px;
# }

# /* File uploader label */
# div[data-testid="stFileUploader"] > label,
# div[data-testid="stFileUploader"] p {
#     font-family: 'Rajdhani', sans-serif !important;
#     font-size: 20px !important;
#     font-weight: 600 !important;
#     letter-spacing: 3px !important;
#     text-transform: uppercase !important;
#     color: #00e5ff !important;
#     margin-bottom: 14px !important;
# }

# section[data-testid="stFileUploaderDropzone"] {
#     border: 2px dashed rgba(0, 200, 122, 0.35) !important;
#     background: rgba(0,200,122,0.04) !important;
#     border-radius: 10px !important;
# }

# section[data-testid="stFileUploaderDropzone"] p,
# section[data-testid="stFileUploaderDropzone"] span {
#     font-family: 'Exo 2', sans-serif !important;
#     color: rgba(255,255,255,0.55) !important;
#     font-size: 15px !important;
# }

# .stDownloadButton > button {
#     font-family: 'Rajdhani', sans-serif !important;
#     font-size: 15px !important;
#     font-weight: 600 !important;
#     letter-spacing: 2px !important;
#     text-transform: uppercase !important;
#     background: linear-gradient(135deg, rgba(0,200,122,0.15), rgba(0,229,255,0.1)) !important;
#     border: 1px solid rgba(0,200,122,0.5) !important;
#     color: #00c87a !important;
#     border-radius: 8px !important;
#     padding: 10px 24px !important;
#     transition: all 0.3s !important;
# }

# .stDownloadButton > button:hover {
#     background: linear-gradient(135deg, rgba(0,200,122,0.3), rgba(0,229,255,0.2)) !important;
#     border-color: #00c87a !important;
#     box-shadow: 0 0 16px rgba(0,200,122,0.3) !important;
#     color: #ffffff !important;
# }

# .stSpinner > div {
#     border-top-color: #00c87a !important;
# }

# div[data-testid="stProgressBar"] > div > div {
#     background: linear-gradient(90deg, #00c87a, #00e5ff) !important;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---------------- HEADER ----------------
# st.markdown("""
# <div class="header-wrap">
#     <div class="badge-line">⬡ neural surveillance system v2.0 ⬡</div>
#     <div class="main-title">Traffic Violation<br>Detection</div>
#     <div class="sub-title">AI-Powered Road Safety Intelligence</div>
# </div>
# <div class="divider"></div>
# """, unsafe_allow_html=True)

# # ---------------- LOAD MODELS ----------------
# @st.cache_resource
# def load_models():
#     helmet = YOLO("runs/detect/train/weights/best.pt")
#     general = YOLO("yolov8n.pt")
#     return helmet, general

# helmet_model, general_model = load_models()

# # ---------------- HELPER: encode image for download ----------------
# def encode_image_to_bytes(img_bgr):
#     """Convert BGR numpy array to PNG bytes for download."""
#     success, buffer = cv2.imencode('.png', img_bgr)
#     if success:
#         return buffer.tobytes()
#     return None

# # ---------------- MODE SELECTION ----------------
# mode = st.radio("📌 SELECT INPUT MODE", ["Image", "Video"], horizontal=True)

# # =====================================================
# # ================= IMAGE SECTION =====================
# # =====================================================

# if mode == "Image":

#     uploaded_file = st.file_uploader("📷 UPLOAD TRAFFIC IMAGE", type=["jpg", "jpeg", "png"])

#     if uploaded_file is not None:

#         file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
#         frame = cv2.imdecode(file_bytes, 1)

#         violation_messages = []
#         no_helmet_detected = False
#         triple_riding_detected = False

#         helmet_results = helmet_model(frame, conf=0.6, verbose=False)

#         for box in helmet_results[0].boxes:
#             class_id = int(box.cls[0])
#             class_name = helmet_results[0].names[class_id]
#             if class_name == "Without Helmet":
#                 no_helmet_detected = True

#         general_results = general_model(frame, conf=0.4, verbose=False)

#         persons = []
#         motorcycles = []

#         for box in general_results[0].boxes:
#             class_id = int(box.cls[0])
#             class_name = general_results[0].names[class_id]
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             if class_name == "person":
#                 persons.append((x1, y1, x2, y2))
#             if class_name in ["motorcycle", "motorbike"]:
#                 motorcycles.append((x1, y1, x2, y2))

#         for bike in motorcycles:
#             bx1, by1, bx2, by2 = bike
#             count = 0
#             for person in persons:
#                 px1, py1, px2, py2 = person
#                 if px1 < bx2 and px2 > bx1 and py1 < by2 and py2 > by1:
#                     count += 1
#             if count > 2:
#                 triple_riding_detected = True
#                 break

#         if no_helmet_detected:
#             violation_messages.append("❌ No Helmet Detected")
#         if triple_riding_detected:
#             violation_messages.append("👥 Triple Riding Detected")

#         if violation_messages:
#             st.markdown(f'<div class="violation-banner">🚨 Traffic Violation Detected — {" · ".join(violation_messages)}</div>', unsafe_allow_html=True)
#             annotated_frame = helmet_results[0].plot()

#             st.markdown('<div class="violation-label">⬡ Annotated Frame</div>', unsafe_allow_html=True)
#             st.image(annotated_frame, channels="BGR", use_container_width=True)

#             # Download button
#             img_bytes = encode_image_to_bytes(annotated_frame)
#             if img_bytes:
#                 st.download_button(
#                     label="⬇  Download Violation Frame",
#                     data=img_bytes,
#                     file_name="violation_frame.png",
#                     mime="image/png"
#                 )
#         else:
#             st.markdown('<div class="safe-banner">✅ No Violation Detected — Road Looks Clear</div>', unsafe_allow_html=True)
#             st.image(frame, channels="BGR", use_container_width=True)


# # =====================================================
# # ================= VIDEO SECTION =====================
# # =====================================================

# if mode == "Video":

#     uploaded_file = st.file_uploader("🎥 UPLOAD TRAFFIC VIDEO", type=["mp4", "avi", "mov"])

#     if uploaded_file:

#         temp_video = tempfile.NamedTemporaryFile(delete=False)
#         temp_video.write(uploaded_file.read())

#         cap = cv2.VideoCapture(temp_video.name)

#         helmet_saved = False
#         triple_saved = False
#         helmet_image = None
#         triple_image = None

#         frame_id = 0
#         frame_skip = 5
#         start_time = time.time()

#         total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         progress_bar = st.progress(0)

#         with st.spinner("🔍 Analyzing video feed..."):

#             while True:
#                 ret, frame = cap.read()
#                 if not ret:
#                     break

#                 frame_id += 1
#                 progress_bar.progress(min(frame_id / total_frames, 1.0))

#                 if frame_id % frame_skip != 0:
#                     continue

#                 frame = cv2.resize(frame, (640, 480))

#                 if not helmet_saved:
#                     helmet_results = helmet_model(frame, conf=0.6, verbose=False)
#                     for box in helmet_results[0].boxes:
#                         class_id = int(box.cls[0])
#                         class_name = helmet_results[0].names[class_id]
#                         if class_name == "Without Helmet":
#                             helmet_saved = True
#                             helmet_image = helmet_results[0].plot()
#                             break

#                 if not triple_saved:
#                     general_results = general_model(frame, conf=0.4, verbose=False)
#                     persons = []
#                     motorcycles = []

#                     for box in general_results[0].boxes:
#                         class_id = int(box.cls[0])
#                         class_name = general_results[0].names[class_id]
#                         x1, y1, x2, y2 = map(int, box.xyxy[0])
#                         if class_name == "person":
#                             persons.append((x1, y1, x2, y2))
#                         if class_name in ["motorcycle", "motorbike"]:
#                             motorcycles.append((x1, y1, x2, y2))

#                     for bike in motorcycles:
#                         bx1, by1, bx2, by2 = bike
#                         count = 0
#                         for person in persons:
#                             px1, py1, px2, py2 = person
#                             if px1 < bx2 and px2 > bx1 and py1 < by2 and py2 > by1:
#                                 count += 1
#                         if count > 2:
#                             triple_saved = True
#                             triple_image = general_results[0].plot()
#                             break

#                 if helmet_saved and triple_saved:
#                     break

#         cap.release()
#         end_time = time.time()

#         processing_time = round(end_time - start_time, 2)

#         st.markdown(f"""
#         <div class="safe-banner" style="background: rgba(0,229,255,0.07); border-color: rgba(0,229,255,0.3); color: #00e5ff;">
#             ✅ Processing Complete &nbsp;·&nbsp;
#             <span class="stat-chip">⏱ {processing_time}s</span>
#             <span class="stat-chip">📽 {frame_id} frames</span>
#         </div>
#         """, unsafe_allow_html=True)

#         if helmet_image is not None:
#             st.markdown('<div class="violation-banner">🚨 No Helmet Violation Detected</div>', unsafe_allow_html=True)
#             st.markdown('<div class="violation-label">⬡ Captured Violation Frame</div>', unsafe_allow_html=True)
#             st.image(helmet_image, channels="BGR", use_container_width=True)

#             img_bytes = encode_image_to_bytes(helmet_image)
#             if img_bytes:
#                 st.download_button(
#                     label="⬇  Download No-Helmet Violation Frame",
#                     data=img_bytes,
#                     file_name="no_helmet_violation.png",
#                     mime="image/png",
#                     key="dl_helmet"
#                 )

#         if triple_image is not None:
#             st.markdown('<div class="violation-banner" style="margin-top: 28px;">🚨 Triple Riding Violation Detected</div>', unsafe_allow_html=True)
#             st.markdown('<div class="violation-label">⬡ Captured Violation Frame</div>', unsafe_allow_html=True)
#             st.image(triple_image, channels="BGR", use_container_width=True)

#             img_bytes = encode_image_to_bytes(triple_image)
#             if img_bytes:
#                 st.download_button(
#                     label="⬇  Download Triple Riding Violation Frame",
#                     data=img_bytes,
#                     file_name="triple_riding_violation.png",
#                     mime="image/png",
#                     key="dl_triple"
#                 )

#         if helmet_image is None and triple_image is None:
#             st.markdown('<div class="safe-banner">✅ No Violations Detected in This Video</div>', unsafe_allow_html=True)

# # ---------------- FOOTER ----------------
# st.markdown('<div class="footer-text">⬡ TRAFFIC VIOLATION DETECTION SYSTEM · AI POWERED · ROAD SAFETY MODULE ⬡</div>', unsafe_allow_html=True)
#------------------------------------------------------
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