import streamlit as st
import cv2
import numpy as np
from tempfile import NamedTemporaryFile
import time

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

    fuente = st.radio("🎥 Fuente de video:", ["Cámara", "Subir archivo"])
    video_file = None
    if fuente == "Subir archivo":
        video_file = st.file_uploader("📂 Sube un video (MP4, AVI, MOV)", type=["mp4", "avi", "mov"])

    iniciar = st.button("🚀 Iniciar Efecto de Realidad Aumentada")

    if iniciar:
        if fuente == "Cámara":
            cap = cv2.VideoCapture(0)
            ejecutar_realidad_aumentada(cap)
        elif video_file:
            temp_file = NamedTemporaryFile(delete=False)
            temp_file.write(video_file.read())
            cap = cv2.VideoCapture(temp_file.name)
            ejecutar_realidad_aumentada(cap)
        else:
            st.warning("⚠️ Selecciona una fuente de video antes de iniciar.")

    st.markdown("---\n✅ **Alumna:** 🦉 Zanabria Yrigoin, Gaby Lizeth")


# ======================================================
# 🔧 Función principal — Realidad Aumentada basada en color
# ======================================================
def ejecutar_realidad_aumentada(cap):
    scaling_factor = 0.6
    stframe_main = st.empty()

    st.info("🔵 Detectando color azul y aplicando efecto de realidad aumentada...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 🎨 Rango del color azul (ajustable según la iluminación)
        lower_blue = np.array([100, 120, 70])
        upper_blue = np.array([140, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        overlay = frame.copy()
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # evita ruido
                # 💫 Efecto de color dinámico (tipo AR)
                color = (
                    int(128 + 127 * np.sin(time.time() * 2)),
                    int(128 + 127 * np.sin(time.time() * 3)),
                    int(255)  # Azul dominante
                )
                cv2.drawContours(overlay, [contour], -1, color, -1)

        # Mezclar overlay con transparencia
        alpha = 0.5
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        stframe_main.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                           caption="🌈 Realidad Aumentada sobre Color Azul",
                           channels="RGB", use_container_width=True)

        time.sleep(0.03)

    cap.release()
