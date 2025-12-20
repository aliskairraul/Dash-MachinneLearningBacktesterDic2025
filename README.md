# Dashboard de Backtesting con Machine Learning

## Visión General

**Dashboard de Backtesting con Machine Learning** es una aplicación interactiva construida con **Dash** que visualiza predicciones y resultados de back‑testing de modelos de aprendizaje automático y profundo aplicados a instrumentos financieros. Integra la adquisición de datos, inferencia de modelos y una interfaz rica para que analistas e inversores exploren el rendimiento de la cartera, tasas de acierto de los modelos y simulaciones de operaciones diarias.

---

## Características Principales

- **Evaluación multi‑instrumento**: S&P 500, EURUSD, BTCUSD, XAUUSD.
- **Pipeline de datos**:
  - Recolección automática diaria mediante web‑scraping y peticiones a Apis públicas.
  - Repositorios separados para datos crudos (`Actualiza-Data-Instrumentos`) y predicciones de modelos (`Inferencias_instrumentos_dic_2025`).
- **Conjunto de modelos**:
  - Implementaciones con **scikit‑learn**, **LightGBM**, **XGBoost**, **PyTorch** y **TensorFlow**.
  - Cada modelo predice la *dirección* del precio del día siguiente.
- **Motor de back‑testing**:
  - Simula una única operación diaria por instrumento.
  - Asignación de capital basada en la confianza del modelo y votación mayoritaria.
  - Métricas detalladas: tasa de acierto, beneficio, número de operaciones diarias, proyección anualizada.
- **Dashboard interactivo**:
  - Gráfico de dona que muestra la composición de la cartera.
  - Resumen de desempeño (beneficio, tasa de acierto, número de operaciones).
  - Métricas por instrumento y gráficos de barras de tasas de acierto.
  - Evolución diaria de la cartera y del capital por instrumento.
  - Vista de operaciones día a día con simulaciones específicas de cada modelo.
- **Arquitectura extensible**: Fácil añadir nuevos instrumentos, fuentes de datos o familias de modelos.

---

## Estructura del Proyecto

```
pro-machinne-dash/
│   README.md               # <-- este archivo
│   main.py                 # Punto de entrada de Dash
│   ayuda.txt               # Descripción del proyecto (fuente de este README)
│   utils/
│       utils.py           # Variables globales y otros
│   functions/             # Funciones Carga/Transformación/Backtesting, Funciones callbacks de Dash
│   components/            # Componentes individuales de Dash (tarjetas, gráficos, etc.)
│   assets/                # Recursos estáticos (imágenes, CSS)
│   .gitignore
│   requirements.txt        # Dependencias de Python
```

---

## Fuentes de Datos

| Instrumento | URL del archivo Parquet |
|------------|------------------------|
| BTCUSD | `https://raw.githubusercontent.com/aliskairraul/Actualiza-Data-Instrumentos/main/db/btcusd-D1_2010-07-17_actualidad.parquet` |
| EURUSD | `https://raw.githubusercontent.com/aliskairraul/Actualiza-Data-Instrumentos/main/db/eurusd-D1_2000-01-03_actualidad.parquet` |
| SPX (S&P 500) | `https://raw.githubusercontent.com/aliskairraul/Actualiza-Data-Instrumentos/main/db/sp500-D1_2000-01-03_actualidad.parquet` |
| XAUUSD | `https://raw.githubusercontent.com/aliskairraul/Actualiza-Data-Instrumentos/main/db/xauusd-D1_2000-01-03_actualidad.parquet` |

Los archivos de predicciones de los modelos se encuentran en el repositorio **Inferencias_instrumentos_dic_2025** y siguen una estructura de URL similar.

---

## Estrategia de Back‑testing

1. **Capital inicial**: $10 000, dividido equitativamente entre los cuatro instrumentos principales.
2. **Decisión diaria**:
   - Cada modelo vota **Invertir** o **No invertir**.
   - Si al menos un modelo vota *Invertir*, el capital disponible para ese instrumento se reparte equitativamente entre los modelos que votaron.
   - La votación mayoritaria determina la dirección (larga/corta). Si la votación está dividida, se asigna una fracción proporcional del capital al lado ganador.
3. **Ejecución**:
   - Una operación por instrumento al día.
   - Se contabilizan los costos de transacción.
4. **Métricas**:
   - Tasa de acierto, beneficio acumulado, número de operaciones diarias y proyección anualizada.

---

## Primeros Pasos

### Requisitos Previos

- Python 3.9+ (probado en 3.11)
- `pip` o `conda`

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/aliskairraul/MachinneLearningBacktesterDic2025.git
cd MachinneLearningBacktesterDic2025

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar el Dashboard

```bash
python main.py
```

Abrir el navegador y navegar a `http://127.0.0.1:8050`.

---

## Extender el Proyecto

- **Añadir nuevos instrumentos**: Actualizar el diccionario de fuentes de datos en `utils.py` y agregar las entradas correspondientes en el layout del dashboard.
- **Integrar modelos adicionales**: Implementar un nuevo script de inferencia, guardar las predicciones en formato Parquet y referenciarlas en el mapa de URLs de predicciones.
- **Personalizar estilo visual**: Modificar `assets/styles.css` o crear nuevos componentes de Dash.

---

## Contribuir

¡Las contribuciones son bienvenidas! Siga estos pasos:
1. Haga un fork del repositorio.
2. Cree una rama de característica (`git checkout -b feature/tu‑característica`).
3. Realice commits con mensajes claros.
4. Abra un pull request describiendo la mejora.

---

## Licencia

Este proyecto se publica bajo la **Licencia MIT**. Consulte el archivo `LICENSE` para más detalles.

---

## Contacto

- **Autor**: *Aliskair Rosríguez*
- **GitHub**: https://github.com/aliskairraul
- **Email**: aliskairraul@gmail.com
- **Desplegado**: https://ef5576ef-9622-420c-8f49-8e5f7facc205.plotly.app

---

*Potencie sus decisiones de inversión con información basada en datos y modelos de machine‑learning de última generación.*
