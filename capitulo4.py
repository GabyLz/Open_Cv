import streamlit as st
import cv2
import numpy as np
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# ============================
# Carga de clasificador Haar
# ============================
face_cascade = cv2.CascadeClassifier('./cascade_files/haarcascade_frontalface_alt.xml')

# ============================
# Función para detección de caras en imágenes
# ============================
def detect_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
    return img

# ============================
# Clase para stream en vivo
# ============================
class FaceDetector(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        return detect_faces(img)

# ============================
# App principal
# ============================
def app():
    st.title("📕 Capítulo 4 — Face Detector (Imagen/Video)")
    st.info("🙂 En este capítulo podrás **detectar rostros** desde una imagen, una foto tomada con la cámara o un stream de video en vivo.")

    fuente = st.radio(
        "Selecciona la fuente de la imagen:",
        ["📂 Subir imagen", "📸 Tomar foto", "📹 Video en vivo (Stream)"],
        horizontal=True
    )

    frame = None

    # ------------------------------
    # Subida de imagen
    # ------------------------------
    if fuente == "📂 Subir imagen":
        uploaded_file = st.file_uploader("Sube tu imagen", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # ------------------------------
    # Foto estática con cámara
    # ------------------------------
    elif fuente == "📸 Tomar foto":
        camera_file = st.camera_input("Toma una foto con la cámara web")
        if camera_file is not None:
            file_bytes = np.asarray(bytearray(camera_file.read()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # ------------------------------
    # Video en vivo con streamlit-webrtc
    # ------------------------------
    elif fuente == "📹 Video en vivo (Stream)":
        st.markdown("🎥 Streaming en vivo desde la cámara (usa WebRTC en el navegador).")
        webrtc_streamer(
            key="face-detector",
            video_transformer_factory=FaceDetector,
            media_stream_constraints={"video": True, "audio": False},
        )

    # ------------------------------
    # Procesamiento de imagen estática
    # ------------------------------
    if frame is not None and fuente != "📹 Video en vivo (Stream)":
        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Imagen original", use_container_width=True)
        st.divider()
        st.subheader("🙂 Resultado de detección de caras")

        output = detect_faces(frame.copy())
        st.image(cv2.cvtColor(output, cv2.COLOR_BGR2RGB), caption="Caras detectadas", use_container_width=True)

        st.markdown("---\n✅ **Alumna:** 🦉Zanabria Yrigoin, Gaby Lizeth")
