import streamlit as st
import cv2
import numpy as np

def app():
    st.title("📘 Capítulo 1 — Transformaciones Geométricas")

    # Subida de imagen
    uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Convertir archivo a imagen de OpenCV
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(img_rgb, caption="🖼️ Imagen original", use_container_width=True)

        st.divider()
        st.subheader("⚙️ Ajustes de transformación")

        # Explicación visual breve
        with st.expander("ℹ️ ¿Qué hace cada control?"):
            st.markdown("""
            - **Rotación (°)** → Gira la imagen en sentido horario o antihorario.  
              Ejemplo: valores positivos giran hacia la derecha, negativos hacia la izquierda.
            - **Escala** → Aumenta (>1) o reduce (<1) el tamaño de la imagen.  
              Ejemplo: 0.5 reduce a la mitad, 2.0 duplica el tamaño.
            - **Desplazamiento horizontal (tx)** → Mueve la imagen hacia la derecha (positivo) o izquierda (negativo).  
            - **Desplazamiento vertical (ty)** → Mueve la imagen hacia abajo (positivo) o hacia arriba (negativo).
            """)

        # Sliders interactivos con descripciones visuales
        rotation = st.slider("🔄 Rotación (grados)", -180, 180, 0, help="Gira la imagen en grados, en sentido horario o antihorario.")
        scale = st.slider("🔍 Escala", 0.1, 2.0, 1.0, help="Cambia el tamaño de la imagen. Menos de 1 la reduce, más de 1 la amplía.")
        tx = st.slider("↔️ Desplazamiento horizontal", -200, 200, 0, help="Mueve la imagen hacia los lados.")
        ty = st.slider("↕️ Desplazamiento vertical", -200, 200, 0, help="Mueve la imagen hacia arriba o abajo.")

        # Matriz de rotación + escala
        (h, w) = img.shape[:2]
        M = cv2.getRotationMatrix2D((w // 2, h // 2), rotation, scale)

        # Aplicar traslación
        M[0, 2] += tx
        M[1, 2] += ty

        # Transformar la imagen
        transformed = cv2.warpAffine(img, M, (w, h))
        transformed_rgb = cv2.cvtColor(transformed, cv2.COLOR_BGR2RGB)

        st.image(transformed_rgb, caption="📐 Imagen transformada", use_container_width=True)

        #
        st.markdown("""
        ---
        ✅ **Alumna:**  
        🦉Zanabria Yrigoin, Gaby Lizeth
        """)

    else:
        st.info("⬆️ Por favor, sube una imagen para comenzar.")
