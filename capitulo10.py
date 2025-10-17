import streamlit as st
import cv2
import numpy as np
import time
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# ======================================================
# 📘 Capítulo 10 — Realidad Aumentada sobre Color
# ======================================================
def app():
    st.title("📘 Capítulo 10 — Realidad Aumentada con Detección de Color")
    st.info("""
    En este capítulo exploraremos un efecto de **realidad aumentada (AR)** 
    usando **OpenCV**, basado en la detección de color.

    **Contenidos:**
    - 🎨 Detección del color azul en tiempo real
    - 🌈 Aplicación de efectos visuales dinámicos
    - 🧠 Superposición tipo realidad aumentada
    """)

    fuente = st.radio(
        "🎥 Fuente de video:",
        ["📹 Cámara en vivo (Stream)", "📂 Subir archivo de video"],
        horizontal=True
    )

    video_file = None
    if fuente == "📂 Subir archivo de video":
        video_file = st.file_uploader("📂 Sube un video (MP4, AVI, MOV)", type=["mp4", "avi", "mov"])

    if fuente == "📹 Cámara en vivo (Stream)":
        st.success("🎥 Cámara en vivo activada. ¡Disfruta del efecto AR!")
        webrtc_streamer(
            key="ar-color",
            video_transformer_factory=ColorARTransformer,
            media_stream_constraints={"video": True, "audio": False},
        )

    elif video_file:
        ejecutar_realidad_aumentada(video_file)

    st.markdown("---\n✅ **Alumna:** 🦉 Zanabria Yrigoin, Gaby Lizeth")


# ======================================================
# 🧠 Clase que aplica el efecto AR en tiempo real
# ======================================================
class ColorARTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        scaling_factor = 0.6
        img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor)

        # Convertir a HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 🎨 Rango del color azul
        lower_blue = np.array([100, 120, 70])
        upper_blue = np.array([140, 255, 255])

        # Crear máscara y buscar contornos
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Crear una capa de superposición
        overlay = img.copy()
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:
                # Color dinámico tipo AR
                color = (
                    int(128 + 127 * np.sin(time.time() * 2)),
                    int(128 + 127 * np.sin(time.time() * 3)),
                    255
                )
                cv2.drawContours(overlay, [contour], -1, color, -1)

        # Mezclar la capa con transparencia
        alpha = 0.5
        output = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        return output


# ======================================================
# 📂 Procesamiento de un archivo de video subido
# ======================================================
def ejecutar_realidad_aumentada(video_file):
    import tempfile

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(video_file.read())
    cap = cv2.VideoCapture(temp_file.name)
    scaling_factor = 0.6
    stframe_main = st.empty()

    st.info("🔵 Detectando color azul y aplicando efecto de realidad aumentada...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([100, 120, 70])
        upper_blue = np.array([140, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        overlay = frame.copy()
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:
                color = (
                    int(128 + 127 * np.sin(time.time() * 2)),
                    int(128 + 127 * np.sin(time.time() * 3)),
                    255
                )
                cv2.drawContours(overlay, [contour], -1, color, -1)

        alpha = 0.5
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        stframe_main.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                           caption="🌈 Realidad Aumentada sobre Color Azul",
                           channels="RGB", use_container_width=True)

        time.sleep(0.03)

    cap.release()
