import streamlit as st
import cv2
import numpy as np
import time
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

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

    fuente = st.radio("🎥 Fuente de video:", ["Cámara en vivo", "Subir archivo"])
    video_file = None

    if fuente == "Subir archivo":
        video_file = st.file_uploader("📂 Sube un video (MP4, AVI, MOV)", type=["mp4", "avi", "mov"])

    # --- Usamos st.session_state para mantener el estado ---
    if "run_ar" not in st.session_state:
        st.session_state.run_ar = False

    if st.button("🚀 Iniciar Efecto de Realidad Aumentada"):
        st.session_state.run_ar = True

    if st.button("⏹️ Detener"):
        st.session_state.run_ar = False

    # ======================================================
    # 📹 Control de cámara
    # ======================================================
    if st.session_state.run_ar:
        if fuente == "Cámara en vivo":
            st.success("🎥 Cámara en vivo activada. ¡Disfruta del efecto AR!")
            webrtc_streamer(
                key="ar-color",
                video_processor_factory=ColorARProcessor,
                media_stream_constraints={"video": True, "audio": False},
            )
        elif video_file:
            ejecutar_realidad_aumentada(video_file)
        else:
            st.warning("⚠️ Selecciona una fuente de video antes de iniciar.")

    st.markdown("---\n✅ **Alumna:** 🦉 Zanabria Yrigoin, Gaby Lizeth")


# ======================================================
# 🧠 Procesador para streamlit-webrtc (detección AR en tiempo real)
# ======================================================
class ColorARProcessor(VideoProcessorBase):
    def __init__(self):
        self.scaling_factor = 0.6

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # Redimensionar
        img = cv2.resize(img, None, fx=self.scaling_factor, fy=self.scaling_factor)

        # Convertir a HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 🎨 Rango del color azul
        lower_blue = np.array([100, 120, 70])
        upper_blue = np.array([140, 255, 255])

        # Crear máscara
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        overlay = img.copy()
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:
                color = (
                    int(128 + 127 * np.sin(time.time() * 2)),
                    int(128 + 127 * np.sin(time.time() * 3)),
                    255
                )
                cv2.drawContours(overlay, [contour], -1, color, -1)

        # Transparencia
        alpha = 0.5
        output = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        return output


# ======================================================
# 📂 Procesar un archivo de video (subido)
# ======================================================
def ejecutar_realidad_aumentada(video_file):
    import tempfile
    from tempfile import NamedTemporaryFile

    temp_file = NamedTemporaryFile(delete=False)
    temp_file.write(video_file.read())
    cap = cv2.VideoCapture(temp_file.name)
    scaling_factor = 0.6
    stframe_main = st.empty()

    st.info("🔵 Detectando color azul y aplicando efecto de realidad aumentada...")

    while cap.isOpened() and st.session_state.run_ar:
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
