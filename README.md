# FleetControlAI - Transporte Inteligente y Seguridad Vial

Solución basada en **FiftyOne (Voxel51)** para el monitoreo, supervisión y análisis de flotas de transporte terrestre usando inteligencia artificial, visión artificial y datos geoespaciales.

## Contexto

Las empresas de transporte deben garantizar operaciones seguras, eficientes y trazables mientras cumplen con regulaciones de seguridad vial y mantienen una comunicación constante entre conductores, vehículos y centros de control. Gracias a tecnologías como GPS, visión artificial, sensores, asistentes de voz e inteligencia artificial, hoy es posible construir soluciones que ayuden a prevenir incidentes, optimizar rutas y mejorar la toma de decisiones en tiempo real.

## Rubricas cubiertas

| Rubrica | Implementacion |
|---|---|
| **Supervision inteligente de flotas** | Deteccion de objetos (vehiculos, peatones, senales) en cada captura con bounding boxes y estadisticas por zona via FiftyOne + grafico de barras en dashboard |
| **Comunicacion inteligente con centros de control** | FiftyOne App como torre de control con mapa interactivo + plugin **@copiloto/fleet-control-ai** con 3 paneles + dashboard web independiente en `src/` |
| **Monitoreo de velocidad y cumplimiento de rutas** | Geo-cerca virtual (Manhattan) que filtra capturas dentro/fuera del perimetro autorizado con `geo_within()` |
| **Prediccion de retrasos y eventos operativos** | Analisis de densidad de objetos por zona geografica (Times Square proximity), distribucion de clases detectadas, y mapa de calor de ubicaciones |

## Arquitectura

```
├── .env                        # Credenciales MongoDB Atlas (NO committear)
├── .gitignore
├── requirements.txt            # Dependencias Python
├── README.md
├── scripts/
│   ├── main.py                 # Entry point - Centro de Control
│   └── control_center.py       # Modulo de analisis de flota
├── plugins/
│   └── copiloto/               # Plugin FiftyOne con paneles personalizados
│       ├── fiftyone.yml        # Manifest del plugin
│       └── __init__.py         # 3 paneles: Dashboard, Geo-cerca, Flota
├── src/                        # Dashboard web standalone
│   ├── index.html              # Pagina principal del centro de control
│   ├── css/
│   │   └── style.css           # Estilos oscuros profesionales
│   └── js/
│       └── dashboard.js        # Graficos y animaciones con Chart.js
├── data/                       # Datasets descargados
├── models/                     # Modelos de IA (futuro)
└── notebooks/                  # Notebooks de analisis (futuro)
```

### Flujo de datos

```
Capturas NYC (BDD100K / quickstart-geo)
    │
    ▼
FiftyOne Dataset (440 samples, 8,620 detecciones)
    │
    ├── location (GeoJSON point)       → Mapa interactivo (FiftyOne App)
    ├── ground_truth (Detections)      → Bounding boxes + clases
    └── num_objects                    → Estadisticas por zona
           │
           ▼
    MongoDB Atlas (Cluster0)
           │
           ├── FiftyOne App (localhost:5151)
           │     ├── Location scatterplot interactivo
            │     ├── FleetControlAI Dashboard panel
            │     ├── FleetControlAI Geo-cerca panel
            │     └── FleetControlAI Flota panel (mapa)
           │
           └── src/index.html (dashboard standalone)
                 ├── Estadisticas de flota
                 ├── Distribucion de clases (Chart.js)
                 ├── Geo-cerca Manhattan (donut chart)
                 └── Densidad por zona (barras)
```

## Requisitos

- Python 3.12+
- MongoDB Atlas cluster (o instancia MongoDB local)
- Navegador web moderno

## Instalacion

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd fiftyone-Transporte-Inteligente

# 2. Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar credenciales MongoDB Atlas
echo 'FIFTYONE_DATABASE_URI="mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net"' > .env
```

> **Importante**: El archivo `.env` contiene credenciales sensibles. Esta en `.gitignore`.

## Uso

```bash
source .venv/bin/activate
python scripts/main.py
```

Esto:
1. Carga dataset `quickstart-geo` (440 imagenes NYC)
2. Conecta a MongoDB Atlas con credenciales de `.env`
3. Calcula estadisticas de flota y analisis geoespacial
4. Registra el plugin FleetControlAI con 3 paneles personalizados
5. Abre el dashboard web standalone en tu navegador
6. Lanza FiftyOne App en `http://localhost:5151`

### Paneles FleetControlAI en FiftyOne App

Una vez abierta la App en localhost:5151:
1. Click en el icono **+** junto a la pestana "Samples"
2. Selecciona cualquiera de los 3 paneles FleetControlAI:
   - **FleetControlAI Dashboard**: metricas generales de flota
   - **FleetControlAI Geo-cerca**: monitoreo dentro/fuera Manhattan
   - **FleetControlAI Flota**: mapa interactivo de ubicaciones

### CLI de FiftyOne

```bash
# Listar comandos disponibles
fiftyone --help

# Listar plugins instalados
fiftyone plugins list

# Lanzar app standalone
fiftyone app launch
```

## Dataset: quickstart-geo

440 imagenes del area de NYC (BDD100K validation split) con:
| Campo | Tipo | Descripcion |
|---|---|---|
| `filepath` | string | Ruta a la imagen |
| `ground_truth` | Detections | Bounding boxes: car, traffic sign, traffic light, person, truck, bus, etc. |
| `location` | GeoLocation | Coordenadas GPS (longitude, latitude) |
| `metadata` | ImageMetadata | Tamano, dimensiones, tipo MIME |
| `num_objects` | int | Numero de objetos detectados (campo computado) |
| `detection_classes` | ListField | Clases unicas presentes (campo computado) |

### Estadisticas del dataset

| Metrica | Valor |
|---|---|
| Muestras | 440 |
| Detecciones totales | 8,620 |
| Promedio por captura | 19.6 |
| Dentro de Manhattan | 141 |
| Fuera de Manhattan | 299 |
| Cercanas a Times Square (5km) | 134 |

## Tecnologias

| Tecnologia | Uso |
|---|---|
| **FiftyOne** (Voxel51) | Vision artificial, analisis de datasets, geo-consulta |
| **MongoDB Atlas** | Base de datos cloud para datasets |
| **Plotly** | Graficos interactivos en paneles FiftyOne |
| **Chart.js** | Graficos en dashboard web standalone |
| **Mapbox / OpenStreetMap** | Mapas base |
| **python-dotenv** | Manejo seguro de credenciales |
| **BDD100K** | Dataset de conduccion urbana |
| **CSS3** | Dashboard oscuro profesional con animaciones |
| **JavaScript (ES6+)** | Graficos interactivos y animaciones |
| **HTML5** | Pagina web standalone del centro de control |

## Plugin FleetControlAI

El plugin `@copiloto/guardian-drive-ai` proporciona 3 paneles personalizados dentro de la FiftyOne App:

### 1. FleetControlAI Dashboard (`@copiloto/fleet-control-ai`)
Metricas generales: muestras, detecciones totales, promedio por captura, y grafico de barras con distribucion de clases detectadas.

### 2. FleetControlAI Geo-cerca
Analisis de cumplimiento de rutas: vehiculos dentro/fuera del perimetro de Manhattan con grafico de dona.

### 3. FleetControlAI Flota
Mapa interactivo con todas las ubicaciones GPS de las capturas, marcador de Times Square, y conteo de muestras cercanas.

## Instalación de plugins oficiales de FiftyOne (opcional)

Puedes descargar e instalar los plugins oficiales de FiftyOne (Voxel51) desde el repositorio de plugins. Por ejemplo, para descargar e instalar los plugins que se usaron en este taller:

```bash
# activar el entorno virtual
source .venv/bin/activate

# descargar e instalar plugins desde el repo de Voxel51
fiftyone plugins download https://github.com/voxel51/fiftyone-plugins \
    --plugin-names @voxel51/brain @voxel51/zoo @voxel51/dashboard
```

Verifica los plugins instalados con:

```bash
fiftyone plugins list
```

Los plugins se almacenan en el directorio de plugins de FiftyOne. Usa `fiftyone plugins enable/disable` para activarlos o desactivarlos según necesites.


## Taller: Plugins y paquetes instalados

Ademas del plugin personalizado, el entorno virtual incluye los siguientes plugins y paquetes del ecosistema FiftyOne / Voxel51:

| Plugin / Paquete | Version | Proposito |
|---|---|---|
| **@voxel51/panels** | 1.0.0 | Paneles integrados de FiftyOne App (location scatterplot, embeddings, mapas) |
| **@voxel51/operators** | 1.0.0 | Operadores core de FiftyOne (filtros, consultas, transformaciones) |
| **@voxel51/brain** | n/a | Plugin oficial de Voxel51 para visualización de embeddings y análisis |
| **@voxel51/zoo** | n/a | Colecciones de ejemplo, utilidades y modelos de Voxel51 |
| **@voxel51/dashboard** | n/a | Paneles y componentes adicionales para la FiftyOne App |
| **fiftyone-brain** | 0.22.0 | Visualizacion de embeddings y analisis de datasets |
| **voxel51-eta** | 0.16.0 | Toolkit de vision artificial de Voxel51 |
| **anywidget** | 0.11.0 | Widgets Python interactivos para notebooks y paneles |
| **ipywidgets** | 8.1.8 | Widgets interactivos para Jupyter |
| **plotly** | 6.8.0 | Graficos interactivos en paneles FiftyOne |
| **shapely** | 2.1.2 | Operaciones geoespaciales (geo-cercas, puntos, poligonos) |
| **umap-learn** | 0.5.12 | Reduccion de dimensionalidad para embeddings |
| **ultralytics** | 8.4.71 | Modelos YOLO para deteccion de objetos |
| **ffmpeg-python** | 0.2.0 | Procesamiento de video para dashcams |
| **pymongo** | 4.9.2 | Conexion a MongoDB Atlas |
| **scikit-learn** | 1.9.0 | ML auxiliar (clustering, metricas) |
| **scikit-image** | 0.26.0 | Procesamiento de imagenes |
| **pandas** | 3.0.3 | Manipulacion de datos tabulares |

## Dashboard Web (src/)

El directorio `src/` contiene un dashboard web independiente que se abre automaticamente al ejecutar `main.py`. Incluye:

- **Estadisticas** con animacion de conteo
- **Grafico de barras** con distribucion de objetos detectados
- **Donut chart** con analisis de geo-cerca Manhattan
- **Grafico de densidad** por zona de NYC
- **Rubricas** visualmente detalladas
- Diseño oscuro profesional con CSS3 y animaciones

Para abrirlo manualmente:
```bash
# Abrir directamente
xdg-open src/index.html

# O con servidor Python (recomendado para live reload)
cd src && python3 -m http.server 8080
# Luego abre http://localhost:8080
```

## Proximos pasos

- [ ] Incorporar video en tiempo real desde dashcams
- [ ] Integrar modelo YOLO para deteccion en vivo
- [ ] Sistema de alertas por geocerca violada
- [ ] Plugin TypeScript con build personalizado (React)
- [ ] Panel de KPIs en la FiftyOne App
- [ ] Prediccion de rutas optimas con ML
- [ ] WebSocket para actualizaciones en tiempo real
