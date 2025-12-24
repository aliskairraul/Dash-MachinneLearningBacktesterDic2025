# 🚀 Dashboard de Backtesting con Machine Learning

![Python](https://img.shields.io/badge/Language-Python%203.9%2B-blue)
![Dash](https://img.shields.io/badge/Framework-Dash-blueviolet)
![Machine Learning](https://img.shields.io/badge/Tech-Machine%20Learning-gold)
![Status](https://img.shields.io/badge/Status-Functional-green)

Este proyecto es una aplicación interactiva de alto rendimiento construida con **Dash** para la visualización de predicciones y resultados de backtesting. El sistema integra modelos de Inteligencia Artificial para el análisis de instrumentos financieros, permitiendo explorar el rendimiento de carteras, tasas de acierto y simulaciones de trading diario en un entorno visual profesional.

---

## 📈 Instrumentos Financieros Cubiertos

El dashboard analiza los activos más representativos para una diversificación estratégica:

*   **S&P 500 (SPX):** El índice bursátil más importante de los EE.UU.
*   **EUR/USD:** El par de divisas líder del mercado Forex.
*   **BTC/USD:** La criptomoneda referente frente al dólar.
*   **XAU/USD:** El Oro, el activo refugio por excelencia a nivel global.

---

## 🛠️ Stack Tecnológico y Modelos

Hemos implementado un conjunto robusto de librerías para cubrir diversas arquitecturas de predicción:

*   **Machine Learning (Clásicos & Ensembles)**:
    *   **Sklearn**: Base para preprocesamiento y modelos tradicionales.
    *   **LightGBM**: Algoritmos de gradiente rápido.
    *   **XGBoost**: Clasificación de alto rendimiento.
*   **Deep Learning (Redes Neuronales)**:
    *   **PyTorch**: Modelos de redes neuronales personalizadas.
    *   **TensorFlow**: Implementaciones robustas para series temporales.

---

## ⚙️ Arquitectura del Sistema (El Flujo)

Dada la complejidad del pipeline, el proyecto se divide en **3 subsistemas independientes**:

1.  **Obtención de Datos**: Repositorio [`Actualiza-Data-Instrumentos`](https://github.com/aliskairraul/Actualiza-Data-Instrumentos). Realiza web-scraping y peticiones API diariamente.
2.  **Predicción (Inferencias)**: Repositorio [`Inferencias_instrumentos_dic_2025`](https://github.com/aliskairraul/Inferencias_instrumentos_dic_2025). Procesa la data con modelos pesados (TensorFlow/PyTorch) y persiste los resultados en Parquet.
3.  **Visualización (Este Repositorio)**: El Dashboard de Dash que consume las inferencias y ejecuta el motor de backtesting dinámico.

---

## 🧠 Metodologías de Backtesting

La aplicación permite evaluar el rendimiento del capital mediante tres enfoques estratégicos distintos, adaptables a diferentes perfiles de riesgo:

*   **1. Estrategia Individual**: 
    Se aísla el comportamiento y riesgo de cada modelo dentro del portafolio. Por lo que la decisión de inversión de cada modelo se ejecuta sin tener pendiente el resto de los modelos dentro del instrumento específico.(ej. S&P 500 con la librería TensorFlow). El capital total se asigna a este modelo para validar su capacidad predictiva y rentabilidad en solitario frente al mercado, sería el capital disponible del Instrumento S&P 500 dividido entre el número de modelos en el mismo (independientemente de que ese dia los demas eligan invertir o no).
*   **2. Mayoría Ponderada (Consenso Dinámico)**: 
    Funciona como un sistema de votación democrática entre todas las librerías activas. El tamaño de la posición se ajusta proporcionalmente a la fuerza del consenso. Si existe división (ej. 3 al alza vs 2 a la baja), se opera con una fracción del capital (ej. 20%) reflejando la cautela ante la falta de unanimidad.  De haber unanimidad (así sea de un Voto) se invierte el 100% del Capital disponible para ese instrumento
*   **3. Mayoría Absoluta (Alta Convicción)**: 
    Similar al consenso, pero con una ejecución más agresiva. Siempre que una dirección gane la votación, se invierte la totalidad del monto disponible para ese activo en esa dirección, maximizando el aprovechamiento de las tendencias identificadas por el bloque de modelos.

### Lógica de Operación
*   **Gestión de Capital**: Partimos de un capital inicial de **$10,000**, diversificado equitativamente entre los 4 instrumentos principales.
*   **Filtro de Probabilidad**: No se ejecutan órdenes si el umbral de confianza de la predicción no supera los niveles de seguridad establecidos, priorizando la preservación del capital sobre la sobreoperativa.
*   **Costos Operativos**: El motor de backtesting descuenta automáticamente spreads y comisiones para ofrecer resultados realistas.

---

## 🚀 Próximos Pasos y Evolución

El proyecto se encuentra en una fase de optimización continua. Nuestras líneas de desarrollo futuro incluyen:

*   **🔍 Monitoreo de Consistencia**: Análisis de la estabilidad del WinRate mes a mes para identificar qué modelos (Librería/Instrumento) presentan un comportamiento más robusto en el tiempo.
*   **🌐 Expansión del Portafolio**: Incorporación de nuevos instrumentos (Forex, Materias Primas) que no presenten interdependencia con los actuales para fortalecer la robustez de la diversificación.
*   **⚡ Transición a Tiempo Real**: Evolución hacia infraestructuras de baja latencia que permitan realizar inferencias y ejecuciones de manera inmediata, superando las limitaciones de los flujos de trabajo programados.
*   **🤖 Integración con Bots de Trading**: Desarrollo de APIs de comunicación con terminales de trading para automatizar la ejecución de órdenes basada en las señales de los modelos, combinando análisis cuantitativo con gestión de riesgo avanzada.

---

## 🤝 Contacto y Portafolio

*   **LinkedIn**: [Aliskair Rodriguez](https://www.linkedin.com/in/aliskair-rodriguez-782b3641/)
*   **GitHub**: [@aliskairraul](https://github.com/aliskairraul)
*   **Email**: [aliskairraul@gmail.com](mailto:aliskairraul@gmail.com)
*   **Web/Portfolio**: [aliskairraul.github.io](https://aliskairraul.github.io)
*   **Despliegue Live**: [Plotly Cloud Link](https://ef5576ef-9622-420c-8f49-8e5f7facc205.plotly.app)

---
*Desarrollado con ❤️ para el análisis avanzado de mercados financieros.*
