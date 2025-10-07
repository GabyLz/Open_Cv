import streamlit as st
import cv2
import numpy as np

def app():
    # ==============================
    # 🎨 Estilo visual (Mínimo CSS para asegurar el contraste en modo oscuro)
    # Se añade un bloque para garantizar que el texto en elementos específicos
    # (como el expander o los selectores) sea legible sobre el nuevo fondo oscuro.
    # ==============================



    st.title("📗 Capítulo 2 — Filtros y Detección de Bordes")

    # ==============================
    # 🧠 Explicación general
    # ==============================
    with st.expander("📘 ¿Qué se aprende en este capítulo?"):
        st.markdown("""
        En este capítulo se estudian **filtros espaciales** y **técnicas de detección de bordes**, dos herramientas esenciales del procesamiento digital de imágenes.

        🔹 **Filtros con kernels**: 
        Utilizan matrices pequeñas (*kernels*) para modificar los píxeles y generar efectos como suavizado, enfoque o relieve.

        🔹 **Detección de bordes**: 
        Identifica los contornos principales de una imagen mediante gradientes o diferencias de intensidad.

        ---
        """)

    # ==============================
    # 📤 Subida de imagen
    # ==============================
    uploaded_file = st.file_uploader("📷 Sube una imagen", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        # Convertir de BGR (OpenCV) a RGB (Streamlit)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

        st.image(img_rgb, caption="🖼️ Imagen original", use_container_width=True)
        st.divider()

        # ==============================
        # 🧮 Selección del tipo de operación
        # ==============================
        tipo = st.radio(
            "🧩 Elige una categoría de procesamiento:",
            ["Filtros con Kernels", "Detección de Bordes"],
            horizontal=True
        )

        # ==============================
        # 🌈 FILTROS CON KERNELS
        # ==============================
        if tipo == "Filtros con Kernels":
            filtro = st.selectbox(
                "✨ Selecciona un filtro para aplicar",
                [
                    "Filtro identidad",
                    "Filtro promedio 3x3",
                    "Filtro promedio 5x5",
                    "Desenfoque por movimiento",
                    "Enfocar imagen",
                    "Enfocado fuerte",
                    "Realce de bordes",
                    "Relieve (Emboss)",
                    "Viñeta"
                ],
                index=0
            )

            output = None

            if filtro == "Filtro identidad":
                # Kernel que no modifica la imagen
                kernel = np.array([[0,0,0],[0,1,0],[0,0,0]])
                output = cv2.filter2D(img, -1, kernel)

            elif filtro == "Filtro promedio 3x3":
                # Kernel para suavizado/promedio simple
                kernel = np.ones((3,3), np.float32) / 9
                output = cv2.filter2D(img, -1, kernel)

            elif filtro == "Filtro promedio 5x5":
                # Kernel para suavizado/promedio más fuerte
                kernel = np.ones((5,5), np.float32) / 25
                output = cv2.filter2D(img, -1, kernel)

            elif filtro == "Desenfoque por movimiento":
                # Kernel para 'motion blur'
                size = 15
                kernel_motion = np.zeros((size, size))
                kernel_motion[int((size-1)/2), :] = np.ones(size)
                kernel_motion = kernel_motion / size
                output = cv2.filter2D(img, -1, kernel_motion)

            elif filtro == "Enfocar imagen":
                # Kernel para enfoque (Sharpness)
                kernel_sharp = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                output = cv2.filter2D(img, -1, kernel_sharp)

            elif filtro == "Enfocado fuerte":
                # Kernel para enfoque excesivo
                kernel_excess = np.array([[1,1,1], [1,-7,1], [1,1,1]])
                output = cv2.filter2D(img, -1, kernel_excess)

            elif filtro == "Realce de bordes":
                # Kernel de realce de bordes complejo
                kernel_edge = np.array([
                    [-1,-1,-1,-1,-1],
                    [-1,2,2,2,-1],
                    [-1,2,8,2,-1],
                    [-1,2,2,2,-1],
                    [-1,-1,-1,-1,-1]
                ]) / 8.0
                output = cv2.filter2D(img, -1, kernel_edge)

            elif filtro == "Relieve (Emboss)":
                # Efecto relieve. Se convierte a gris y se añade offset para visibilidad
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                kernel_emboss = np.array([[0,-1,-1],[1,0,-1],[1,1,0]])
                output = cv2.filter2D(gray, -1, kernel_emboss) + 128 

            elif filtro == "Viñeta":
                # Efecto viñeta (oscurecimiento en los bordes)
                rows, cols = img.shape[:2]
                kernel_x = cv2.getGaussianKernel(int(1.5 * cols), 200)
                kernel_y = cv2.getGaussianKernel(int(1.5 * rows), 200)
                kernel = kernel_y * kernel_x.T
                mask = 255 * kernel / np.linalg.norm(kernel)
                mask = mask[int(0.5 * rows):, int(0.5 * cols):]
                
                output = np.copy(img)
                # Aplicar la máscara a cada canal de color
                for i in range(3):
                    output[:,:,i] = cv2.multiply(output[:,:,i], mask.astype(output.dtype), scale=1/255)


            if output is not None:
                # Convertir a RGB solo si la imagen de salida es a color
                if len(output.shape) == 3:
                    output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
                else:
                    output_rgb = output # Ya es monocromático
                st.image(output_rgb, caption=f"🎨 Resultado: {filtro}", use_container_width=True)

        # ==============================
        # ⚙️ DETECCIÓN DE BORDES
        # ==============================
        else:
            # Convertir a escala de grises para todos los detectores de bordes
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            metodo = st.selectbox(
                "🔍 Selecciona el método de detección de bordes:",
                ["Sobel Horizontal", "Sobel Vertical", "Laplaciano", "Canny"],
                index=0
            )

            resultado = None

            if metodo in ["Sobel Horizontal", "Sobel Vertical"]:
                # Configuración de Sobel (dx, dy)
                ksize = st.slider("📏 Tamaño del kernel (1, 3, 5 o 7)", 1, 7, 5, step=2)
                dx, dy = (1, 0) if metodo == "Sobel Horizontal" else (0, 1)
                resultado = cv2.Sobel(gray, cv2.CV_64F, dx, dy, ksize=ksize)

            elif metodo == "Laplaciano":
                # Aplicar Laplaciano
                resultado = cv2.Laplacian(gray, cv2.CV_64F)

            elif metodo == "Canny":
                # Configuración de Canny
                st.write("🔧 Ajusta los umbrales para definir la sensibilidad del detector:")
                min_val = st.slider("🔹 Umbral mínimo", 0, 255, 50)
                max_val = st.slider("🔸 Umbral máximo", 0, 255, 240)
                resultado = cv2.Canny(gray, min_val, max_val)
            
            if resultado is not None:
                # Convertir a 8-bit para visualización
                resultado = cv2.convertScaleAbs(resultado) 
                st.image(resultado, caption=f"📐 Resultado: {metodo}", use_container_width=True)

        # ==============================
        # 📚 Créditos
        # ==============================
        st.markdown("""
        ---
        ✅ **Alumna:** 🦉 Zanabria Yrigoin, Gaby Lizeth
        """)

    else:
        st.info("⬆️ Sube una imagen para aplicar filtros o detectar bordes.")
