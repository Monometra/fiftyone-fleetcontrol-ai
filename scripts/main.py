import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_PYTHON = os.path.join(BASE, ".venv", "bin", "python")

if os.path.exists(VENV_PYTHON) and sys.executable != VENV_PYTHON:
    os.environ["FIFTYONE_DATABASE_URI"] = "mongodb+srv://dkarinamendezd_db_user:lCDnIRb0qQxcNDnw@cluster0.ux8amal.mongodb.net"
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

env_path = os.path.join(BASE, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("\"'"))

import webbrowser

import fiftyone as fo
import fiftyone.zoo as foz

from control_center import (
    load_fleet_data,
    fleet_stats,
    geo_fence_analysis,
    near_point_analysis,
    object_class_summary,
)

TIMES_SQUARE = [-73.9855, 40.7580]
MANHATTAN = [
    [
        [-73.949701, 40.834487],
        [-73.896611, 40.815076],
        [-73.998083, 40.696534],
        [-74.031751, 40.715273],
        [-73.949701, 40.834487],
    ]
]

print("=" * 60)
print("  FleetControlAI - Transporte Inteligente y Seguridad Vial")
print("=" * 60)

dataset = load_fleet_data()

stats = fleet_stats(dataset)
print(f"\nFlota cargada: {stats['samples']} capturas")
print(f"  Objetos detectados: {stats['total_detections']}")
print(f"  Promedio por captura: {stats['avg_objects_per_sample']}")

classes = object_class_summary(dataset)
print("\nClases detectadas:")
for cls, count in classes.most_common(10):
    print(f"  {cls}: {count}")

geo = geo_fence_analysis(dataset, MANHATTAN)
print(f"\nGeo-cerca Manhattan:")
print(f"  Dentro del perimetro: {geo['num_inside']}")
print(f"  Fuera del perimetro: {geo['num_outside']}")

print("\nProximidad Times Square (5km):")
near = near_point_analysis(dataset, TIMES_SQUARE, 5000)
print(f"  Muestras cercanas: {len(near)}")

print("\nIniciando Centro de Control...")
print("  Abre tu navegador en http://localhost:5151")
print()
print("  Rubricas cubiertas:")
print("  \u25cf Supervision inteligente de flotas -> Detecciones por imagen")
print("  \u25cf Comunicacion centros de control -> App + mapa interactivo + plugins")
print("  \u25cf Monitoreo rutas/velocidad -> Geo-cerca Manhattan")
print("  \u25cf Prediccion retrasos/eventos -> Densidad por zona y clase")

print("\n  Paneles FleetControlAI disponibles en la App:")
print("  - FleetControlAI Dashboard: estadisticas generales")
print("  - FleetControlAI Geo-cerca: monitoreo de rutas")
print("  - FleetControlAI Flota: mapa de ubicaciones")

dashboard_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "src", "index.html"
)
webbrowser.open(f"file://{dashboard_path}")
print(f"\n  Dashboard web abierto: file://{dashboard_path}")

session = fo.launch_app(dataset)

try:
    plot = fo.location_scatterplot(
        samples=dataset,
        labels="num_objects",
        sizes="num_objects",
        labels_title="Objetos detectados",
        sizes_title="Objetos",
        map_type="roadmap",
    )
    plot.show()
    session.plots.attach(plot)
except Exception as e:
    print(f"Plot creation failed (non-fatal): {e}")

input("\nPresiona Enter para cerrar...")
