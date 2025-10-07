import streamlit as st
import cv2
import numpy as np

# =========================================
# App principal para Capítulo 5
# =========================================
def app():
    st.title("📕 Capítulo 5 — Feature Extraction")
    st.info("🔍 En este capítulo podrás probar diferentes **detectores y descriptores de características** de OpenCV.")

    # ===============================
    # Selección de algoritmo
    # ===============================
    metodo = st.selectbox(
        "Selecciona el método de extracción de características:",
        [
            "FAST",
            "Shi-Tomasi (goodFeaturesToTrack)",
            "Harris",
            "ORB"
        ]
    )

    # ===============================
    # Subir imagen
    # ===============================
    uploaded_file = st.file_uploader("📂 Sube una imagen", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Imagen original", use_container_width=True)

        # ===============================
        # Algoritmos de extracción
        # ===============================
        output = img.copy()

        if metodo == "FAST":
            fast = cv2.FastFeatureDetector_create()
            kp = fast.detect(gray, None)
            cv2.drawKeypoints(img, kp, output, color=(0,255,0),
                              flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        elif metodo == "Shi-Tomasi (goodFeaturesToTrack)":
            corners = cv2.goodFeaturesToTrack(gray, maxCorners=50, qualityLevel=0.05, minDistance=10)
            if corners is not None:
                for c in corners.astype(int):
                    x, y = c.ravel()
                    cv2.circle(output, (x, y), 5, (0, 255, 0), -1)

        elif metodo == "Harris":
            gray_float = np.float32(gray)
            dst = cv2.cornerHarris(gray_float, blockSize=4, ksize=5, k=0.04)
            dst = cv2.dilate(dst, None)
            output[dst > 0.01 * dst.max()] = [0, 0, 255]

        elif metodo == "ORB":
            orb = cv2.ORB_create()
            kp, des = orb.detectAndCompute(gray, None)
            cv2.drawKeypoints(img, kp, output, color=(0,255,0),
                              flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # ===============================
        # Mostrar resultados
        # ===============================
        st.image(cv2.cvtColor(output, cv2.COLOR_BGR2RGB),
                 caption=f"Resultado con {metodo}", use_container_width=True)

        st.markdown("---\n✅ **Alumna:** 🦉 Zanabria Yrigoin, Gaby Lizeth")
