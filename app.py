import streamlit as st

# Importación de módulos
# (Se asume que estos archivos existen: capitulo1.py, capitulo2.py, etc.)
import capitulo1
import capitulo2
import capitulo3
import capitulo4
import capitulo5
import capitulo6
import capitulo7
import capitulo8
import capitulo9
import capitulo10
import capitulo11

# =====================================
# CONFIGURACIÓN GENERAL
# =====================================
st.set_page_config(
    page_title="Laboratorio de Visión por Computadora",
    page_icon="🧠",
    layout="wide",
)

# =====================================
# ESTILOS PERSONALIZADOS (modo oscuro)
# =====================================
st.markdown("""
    <style>
        /* Sidebar moderno (verde azulado degradado con fondo oscuro) */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #002626 0%, #007f7f 100%);
            color: white !important;
            padding-top: 1.5em;
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
        }

        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] span {
            color: #e0f7fa !important;
        }

        /* Selectbox oscuro con texto claro */
        div[data-baseweb="select"] > div {
            background-color: #003d3d !important;
            border-radius: 10px;
            border: 2px solid #00c2a8;
            color: #ffffff !important;
        }

        /* Botones */
        .stButton>button {
            background: linear-gradient(90deg, #00c2a8 0%, #007f7f 100%);
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            border: none;
            transition: 0.2s;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #009e9e 0%, #004d4d 100%);
            color: #e0f7ff;
        }

        /* Caja explicativa */
        .info-box {
            background-color: #002b2b;
            border-left: 6px solid #00c2a8;
            border-radius: 8px;
            padding: 1em 1.5em;
            color: #e0f7fa;
            margin: 1.5em 0;
        }

        /* Línea divisoria */
        hr, .stMarkdown hr {
            border-color: #00c2a8;
        }
    </style>
""", unsafe_allow_html=True)
# =====================================
# ENCABEZADO
# =====================================
st.markdown("<div class='main-title'>🧠 Laboratorio de Visión por Computadora</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Proyecto modular interactivo con Streamlit + OpenCV</div>", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================
with st.sidebar:
    st.title("📚 Menú de capítulos")
    opcion = st.selectbox(
        "Selecciona un capítulo:",
        [
            "📘 Capítulo 1 — Geometric Transformations",
            "📗 Capítulo 2 — Edges & Filters",
            "📙 Capítulo 3 — Cartoonizing (Webcam/Photo)",
            "📕 Capítulo 4 — Body Parts",
            "📕 Capítulo 5 — Feature Extraction",
            "📒 Capítulo 6 — Seam Carving (Reducción de contenido)",
            "📔 Capítulo 7 — Detección y Aproximación de Contornos",
            "📓 Capítulo 8 — Seguimiento de Objetos por Color",
            "📚 Capítulo 9 — Reconocimiento de Objetos (ORB + BFMatcher)",
            "📖 Capítulo 10 — Realidad Aumentada con Cámara (Detección por color)",
            "📑 Capítulo 11 — Machine Learning (ANN) - Demo con Digits"
        ]
    )

# =====================================
# DESCRIPCIÓN DE CADA CAPÍTULO
# =====================================
st.markdown("---")

if opcion.startswith("📘 Capítulo 1"):
    st.markdown("""
    <div key="desc1" class="info-box">
        <h4>📘 Capítulo 1 — Geometric Transformations</h4>
        <p>En este capítulo podrás experimentar con <b>transformaciones geométricas</b> aplicadas a imágenes. 
        Podrás subir una imagen y modificar su orientación y posición visual en tiempo real mediante:</p>
        <ul>
            <li>🔄 <b>Rotación</b> — gira la imagen en grados (positivos o negativos).</li>
            <li>📏 <b>Escalado</b> — aumenta o reduce el tamaño de la imagen.</li>
            <li>↔️ <b>Traslación</b> — mueve la imagen en direcciones horizontal y vertical.</li>
        </ul>
        <p>Estas operaciones son fundamentales en Visión por Computadora para la alineación, 
        el preprocesamiento y la normalización de imágenes antes de tareas más complejas.</p>
    </div>
    """, unsafe_allow_html=True)

elif opcion.startswith("📗 Capítulo 2"):
    st.markdown("""
    <div key="desc2" class="info-box">
        <h4>📗 Capítulo 2 — Edges & Filters</h4>
        <p>En este capítulo podrás explorar el fascinante mundo de los <b>filtros y detección de bordes</b> 
        en imágenes, una de las bases de la Visión por Computadora. Aquí podrás aplicar distintos operadores 
        de filtrado para resaltar contornos, bordes y transiciones en las imágenes.</p>
        <p>Dispondrás de dos secciones principales:</p>
        <ul>
            <li>🎨 <b>Filtros con núcleos</b> — permiten suavizar o realzar detalles en la imagen usando convolución.</li>
            <li>🧭 <b>Detección de bordes</b> — usa operadores como Sobel, Laplacian y Canny para encontrar cambios bruscos de intensidad.</li>
        </ul>
        <p>Estos métodos son esenciales para el <b>análisis estructural de imágenes</b> y preparan el terreno 
        para tareas como reconocimiento de formas y segmentación.</p>
    </div>
    """, unsafe_allow_html=True)
elif opcion.startswith("📙 Capítulo 3"):
    st.markdown("""
    <div key="desc3" class="info-box">
        <h4>📙 Capítulo 3 — Cartoonizing (Webcam/Photo)</h4>
        <p>En este capítulo podrás transformar tus imágenes o la señal de tu cámara en un 
        <b>estilo caricaturesco</b> aplicando técnicas de filtrado y detección de bordes.</p>
        <p>Dispondrás de dos modos principales:</p>
        <ul>
            <li>📷 <b>Imagen estática</b> — sube una fotografía desde tu computadora y obtén 
            una versión estilo cartoon.</li>
            <li>🎥 <b>Cámara en vivo</b> — usa tu webcam mediante <code>streamlit-webrtc</code> 
            para ver el efecto aplicado en tiempo real.</li>
        </ul>
        <p>Este método se basa en una combinación de <b>suavizado bilateral</b> para simplificar colores 
        y <b>detección de bordes</b> para resaltar contornos, generando un efecto similar al dibujo animado.</p>
    </div>
    """, unsafe_allow_html=True)
elif opcion.startswith("📕 Capítulo 4"):
    st.markdown("""
    <div key="desc4" class="info-box">
        <h4>📕 Capítulo 4 — Face Detector (Imagen/Video)</h4>
        <p>En este capítulo aprenderás a <b>detectar rostros humanos</b> usando el algoritmo 
        <code>Haar Cascade Classifier</code>, un método clásico y rápido para el reconocimiento facial.</p>
        <p>Dispondrás de tres modos principales:</p>
        <ul>
            <li>📂 <b>Subir imagen</b> — selecciona una fotografía desde tu computadora para detectar rostros.</li>
            <li>📸 <b>Tomar foto</b> — captura una imagen directamente con tu cámara web.</li>
            <li>📹 <b>Video en vivo</b> — usa <code>streamlit-webrtc</code> para ver la detección en tiempo real.</li>
        </ul>
        <p>El detector funciona convirtiendo la imagen a escala de grises y aplicando un modelo entrenado 
        para localizar patrones característicos de un rostro (ojos, nariz, proporciones faciales). 
        Se dibuja un rectángulo verde alrededor de cada cara detectada.</p>
        <p>⚡ Aunque es un método eficiente, puede verse limitado en condiciones de iluminación pobre 
        o con rostros en ángulos extremos. Más adelante exploraremos detectores más avanzados.</p>
    </div>
    """, unsafe_allow_html=True)    
elif opcion.startswith("📕 Capítulo 5"):
    st.markdown("""
   <div key="desc5" class="info-box">
        <h4>📕 Capítulo 5 — Feature Extraction</h4>
        <p>En este capítulo explorarás cómo <b>detectar puntos clave</b> en una imagen utilizando distintos algoritmos de OpenCV.</p>
        <p>Los métodos disponibles son:</p>
        <ul>
            <li>⚡ <b>FAST</b> — detector muy rápido, ideal para aplicaciones en tiempo real.</li>
            <li>🔹 <b>Shi-Tomasi</b> (<code>goodFeaturesToTrack</code>) — basado en esquinas óptimas para el seguimiento.</li>
            <li>🔸 <b>Harris</b> — detector clásico de esquinas, útil en estructuras geométricas.</li>
            <li>⭐ <b>ORB</b> — detector y descriptor eficiente, alternativa libre a SIFT/SURF.</li>
        </ul>
        <p>Cada método resalta diferentes tipos de puntos característicos como esquinas, bordes o patrones 
        distintivos en la imagen. Estos puntos son fundamentales en tareas de <i>visión por computadora</i> 
        como <b>reconocimiento de objetos</b>, <b>tracking</b> y <b>registro de imágenes</b>.</p>
        <p>📷 Al seleccionar un algoritmo y subir una imagen, verás los <b>puntos clave resaltados</b> 
        en verde o rojo según el método utilizado.</p>
    </div>
    """, unsafe_allow_html=True)
elif opcion.startswith("📒 Capítulo 6"):
    st.markdown("""
   <div key="desc5" class="info-box">
        <h4>📒 Capítulo 6 — Seam Carving (Eliminación de Objetos)</h4>
        <p>En este capítulo aprenderás a utilizar el algoritmo de <b>Seam Carving</b>, una técnica de 
        <i>redimensionamiento inteligente</i> que permite <b>eliminar objetos o reducir dimensiones</b> 
        de una imagen conservando las regiones más importantes.</p>
        <p>El proceso consiste en:</p>
        <ul>
            <li>📊 <b>Cálculo de energía</b> — identifica las zonas más relevantes de la imagen usando gradientes (Sobel).</li>
            <li>✂️ <b>Búsqueda de seams</b> — encuentra caminos de píxeles con menor energía (menos importantes visualmente).</li>
            <li>🚀 <b>Eliminación iterativa</b> — remueve uno o varios seams para reducir ancho o eliminar objetos.</li>
        </ul>
        <p>Este método es ampliamente utilizado en <i>edición de imágenes</i>, permitiendo 
        <b>redimensionar sin distorsión</b> y <b>remover elementos no deseados</b> de manera natural.</p>
        <p>📷 Al subir una imagen y seleccionar el número de <i>seams</i> a eliminar, verás cómo 
        la imagen se adapta automáticamente conservando su contenido principal.</p>
    </div>
    """, unsafe_allow_html=True)
elif opcion.startswith("📔 Capítulo 7"):
    st.markdown("""
   <div key="desc5" class="info-box">
        <h4>📗 Capítulo 7 — Segmentación de Imágenes</h4>
        <p>En este capítulo aprenderás diferentes técnicas clásicas de <b>segmentación</b> 
        en visión por computadora, cuyo objetivo es <b>separar objetos o regiones de interés</b> 
        dentro de una imagen.</p>
        <p>Los métodos que veremos son:</p>
        <ul>
            <li>✂️ <b>GrabCut</b> — separa un objeto del fondo a partir de una selección inicial.</li>
            <li>🔹 <b>Contornos</b> — detecta y dibuja los bordes de las figuras en la imagen.</li>
            <li>🌊 <b>Watershed</b> — algoritmo basado en regiones, ideal para dividir áreas complejas.</li>
        </ul>
        <p>Estos métodos son ampliamente utilizados en <i>procesamiento digital de imágenes</i> 
        para tareas como:</p>
        <ul>
            <li>📌 Extracción de objetos.</li>
            <li>📌 Análisis de formas.</li>
            <li>📌 Preprocesamiento para visión artificial.</li>
        </ul>
        <p>📷 Al subir una imagen podrás seleccionar el método de segmentación deseado 
        y visualizar el resultado en tiempo real.</p>
    </div>
    """, unsafe_allow_html=True)
elif opcion.startswith("📓 Capítulo 8"):
    st.markdown("""
    <div key="desc8" class="info-box">
        <h4>📓 Capítulo 8 — Detección de Movimiento y Color</h4>
        <p>En este capítulo aprenderás a realizar <b>detección de movimiento y color en tiempo real</b> utilizando <code>OpenCV</code> y <code>Streamlit</code>.</p>
        <p>Podrás experimentar con distintos métodos de análisis de video:</p>
        <ul>
            <li>🚶‍♂️ <b>Sustracción de fondo (GMG / MOG2)</b> — detecta objetos en movimiento separándolos del fondo.</li>
            <li>🎨 <b>Detección de color (HSV)</b> — resalta objetos de un color específico, como el azul.</li>
            <li>📸 <b>Diferencia de cuadros</b> — detecta cambios entre imágenes consecutivas para estimar movimiento.</li>
        </ul>
        <p>Esta versión del laboratorio utiliza <b>Streamlit</b> para visualizar los resultados directamente en el navegador, 
        evitando el uso de ventanas emergentes de OpenCV, lo que permite ejecutar el proyecto sin problemas en la nube.</p>
        <p>🔍 A través de estas técnicas podrás entender los principios básicos del <b>seguimiento de objetos</b> y la <b>segmentación dinámica</b> 
        en flujos de video.</p>
    </div>
    """, unsafe_allow_html=True)
elif opcion.startswith("📚 Capítulo 9"):
    st.markdown("""
    <div key="desc9" class="info-box">
        <h4>📚 Capítulo 9 — Clasificación de Imágenes con SIFT y Comparación Directa</h4>
        <p>En este capítulo aprenderás a realizar la <b>comparación y análisis de similitud entre imágenes</b> utilizando el algoritmo 
        <code>SIFT</code> (<i>Scale-Invariant Feature Transform</i>) integrado con <code>OpenCV</code> y <code>Streamlit</code>.</p>
        <p>El objetivo es identificar cuán similares son dos imágenes mediante la detección de características locales 
        y el emparejamiento de descriptores visuales.</p>
        <ul>
            <li>🔍 <b>Extracción de características SIFT</b> — detecta puntos clave robustos ante cambios de escala, rotación e iluminación.</li>
            <li>🧩 <b>Comparación de descriptores</b> — mide la similitud entre imágenes usando un <b>BFMatcher</b> (Brute Force Matcher).</li>
            <li>🔗 <b>Emparejamiento visual</b> — muestra las coincidencias más relevantes entre las dos imágenes cargadas.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif opcion.startswith("📖 Capítulo 10"):
    st.markdown("""
    <div key="desc10" class="info-box">
        <h4>📖 Capítulo 10 — Realidad Aumentada con Detección de Color</h4>
        <p>En este capítulo aprenderás a implementar un efecto de <b>realidad aumentada (AR)</b> 
        mediante la <b>detección de color</b> utilizando <code>OpenCV</code> y <code>Streamlit</code>.</p>
        <p>El objetivo es identificar zonas del color <b>azul</b> en un video o cámara en vivo, y aplicar sobre ellas 
        un <b>efecto visual dinámico</b> que cambia de tonalidad, simulando una experiencia de realidad aumentada.</p>
        <ul>
            <li>🎨 <b>Detección de color en HSV</b> — localiza píxeles dentro del rango correspondiente al color azul.</li>
            <li>🌈 <b>Efecto visual animado</b> — se superpone una capa semitransparente con tonos variables.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
elif opcion.startswith("📑 Capítulo 11"):
    st.markdown("""
    <div key="desc11" class="info-box">
        <h4>📑 Capítulo 11 — Machine Learning (ANN) con Digits</h4>
        <p>En este capítulo aprenderás a entrenar y evaluar una <b>red neuronal artificial (ANN)</b> 
        usando el dataset <code>digits</code> de <code>scikit-learn</code>. Este conjunto de datos contiene 
        imágenes en escala de grises de 8×8 píxeles que representan dígitos escritos a mano (0–9).</p>
        <p>Con esta demo podrás cargar tus propias imágenes y el modelo intentará reconocer el número 
        usando la red entrenada.</p>
        <ul>
            <li>📊 <b>Dataset Digits</b> — imágenes de dígitos manuscritos (8×8 píxeles).</li>
            <li>🧠 <b>Entrenamiento ANN</b> — red neuronal MLP de una capa oculta.</li>
            <li>🔢 <b>Predicción personalizada</b> — posibilidad de subir una imagen y 
            obtener la predicción del modelo.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Selecciona un capítulo para ver su descripción.")

# =====================================
# RUTEO DE CAPÍTULOS
# =====================================
if opcion.startswith("📘 Capítulo 1"):
    capitulo1.app()
elif opcion.startswith("📗 Capítulo 2"):
    capitulo2.app()
elif opcion.startswith("📙 Capítulo 3"):
    capitulo3.app()
elif opcion.startswith("📕 Capítulo 4"):
    capitulo4.app()
elif opcion.startswith("📕 Capítulo 5"):
    capitulo5.app()
elif opcion.startswith("📒 Capítulo 6"):
    capitulo6.app()
elif opcion.startswith("📔 Capítulo 7"):
    capitulo7.app()
elif opcion.startswith("📓 Capítulo 8"):
    capitulo8.app()
elif opcion.startswith("📚 Capítulo 9"):
    capitulo9.app()
elif opcion.startswith("📖 Capítulo 10"):
    capitulo10.app()
elif opcion.startswith("📑 Capítulo 11"):
    capitulo11.app()
else:
    st.warning("⚠️ Selecciona un capítulo válido para comenzar.")
