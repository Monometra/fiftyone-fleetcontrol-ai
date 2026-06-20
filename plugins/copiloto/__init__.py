import fiftyone.operators as foo
import fiftyone.operators.types as types
import fiftyone.zoo as foz
from collections import Counter
import numpy as np


def _get_or_load_dataset():
    import fiftyone as fo

    if fo.dataset_exists("quickstart-geo"):
        return fo.load_dataset("quickstart-geo")
    return foz.load_zoo_dataset("quickstart-geo", persistent=True)


class CopilotoDashboard(foo.Panel):
    @property
    def config(self):
        return foo.PanelConfig(
            name="copiloto_dashboard",
            label="FleetControlAI Dashboard",
            allow_multiple=False,
            surfaces="grid",
        )

    def on_load(self, ctx):
        dataset = _get_or_load_dataset()
        total = len(dataset)
        dets = sum(
            s.ground_truth and len(s.ground_truth.detections) or 0
            for s in dataset
        )

        counts = Counter()
        for s in dataset:
            if s.ground_truth:
                for d in s.ground_truth.detections:
                    counts[d.label] += 1

        top_classes = counts.most_common(8)

        ctx.panel.state.total_samples = total
        ctx.panel.state.total_detections = dets
        ctx.panel.state.avg_per_sample = round(dets / total, 1) if total else 0
        ctx.panel.state.top_classes = dict(top_classes)

        bar_data = [
            {
                "x": [c for c, _ in top_classes],
                "y": [v for _, v in top_classes],
                "type": "bar",
                "marker": {"color": "#2563eb"},
            }
        ]
        ctx.panel.data.class_chart = bar_data
        ctx.panel.state.class_chart_layout = {
            "title": "Objetos detectados por clase",
            "height": 300,
            "margin": {"l": 40, "r": 20, "t": 40, "b": 60},
            "yaxis": {"title": "Cantidad"},
        }

    def render(self, ctx):
        panel = types.Object()

        header = types.LazyFieldView(label="FleetControlAI - Centro de Control")
        panel.view("header", view=header)

        kvs = types.KeyValueView()
        kvs.add("Muestras", ctx.panel.state.total_samples)
        kvs.add("Detecciones", ctx.panel.state.total_detections)
        kvs.add("Promedio por captura", ctx.panel.state.avg_per_sample)
        panel.view("stats", view=kvs)

        col = types.Column()
        col.add("header")
        col.add("stats")
        panel.obj("top_section", view=col)

        class_chart = types.PlotlyView(layout=ctx.panel.state.class_chart_layout)
        panel.obj("class_chart", view=class_chart, label="Distribucion de clases")

        return types.Property(
            panel,
            view=types.GridView(align_x="center", orientation="vertical"),
        )


class CopilotoGeoFence(foo.Panel):
    @property
    def config(self):
        return foo.PanelConfig(
            name="copiloto_geo_fence",
            label="FleetControlAI Geo-cerca",
            allow_multiple=False,
            surfaces="grid",
        )

    def on_load(self, ctx):
        dataset = _get_or_load_dataset()
        manhattan = [
            [
                [-73.949701, 40.834487],
                [-73.896611, 40.815076],
                [-73.998083, 40.696534],
                [-74.031751, 40.715273],
                [-73.949701, 40.834487],
            ]
        ]
        inside = dataset.geo_within(manhattan, location_field="location")
        outside = dataset.exclude(inside)

        inside_dets = sum(
            s.ground_truth and len(s.ground_truth.detections) or 0
            for s in inside
        )
        outside_dets = sum(
            s.ground_truth and len(s.ground_truth.detections) or 0
            for s in outside
        )

        ctx.panel.state.num_inside = len(inside)
        ctx.panel.state.num_outside = len(outside)
        ctx.panel.state.inside_dets = inside_dets
        ctx.panel.state.outside_dets = outside_dets

        pie_data = [
            {
                "labels": ["Dentro Manhattan", "Fuera Manhattan"],
                "values": [len(inside), len(outside)],
                "type": "pie",
                "marker": {
                    "colors": ["#16a34a", "#dc2626"],
                },
            }
        ]
        ctx.panel.data.geo_chart = pie_data
        ctx.panel.state.geo_chart_layout = {
            "title": "Distribucion geo-cerca Manhattan",
            "height": 300,
        }

    def render(self, ctx):
        panel = types.Object()

        header = types.LazyFieldView(label="FleetControlAI - Monitoreo de Rutas")
        panel.view("header", view=header)

        kvs = types.KeyValueView()
        kvs.add("Dentro Manhattan", ctx.panel.state.num_inside)
        kvs.add("Fuera Manhattan", ctx.panel.state.num_outside)
        kvs.add("Detecciones dentro", ctx.panel.state.inside_dets)
        kvs.add("Detecciones fuera", ctx.panel.state.outside_dets)
        panel.view("geo_stats", view=kvs)

        col = types.Column()
        col.add("header")
        col.add("geo_stats")
        panel.obj("top", view=col)

        geo_chart = types.PlotlyView(layout=ctx.panel.state.geo_chart_layout)
        panel.obj("geo_chart", view=geo_chart, label="Geo-cerca")

        return types.Property(
            panel,
            view=types.GridView(align_x="center", orientation="vertical"),
        )


class CopilotoFleetStats(foo.Panel):
    @property
    def config(self):
        return foo.PanelConfig(
            name="copiloto_fleet_stats",
            label="FleetControlAI Flota",
            allow_multiple=False,
            surfaces="grid",
        )

    def on_load(self, ctx):
        dataset = _get_or_load_dataset()
        times_square = [-73.9855, 40.7580]

        try:
            near = dataset.geo_near(
                times_square, max_distance=5000, location_field="location"
            )
            near_count = len(near)
        except Exception:
            near_count = "N/A (requiere indice)"

        all_locations = []
        for s in dataset:
            try:
                loc = s.location.point.coordinates
                all_locations.append(loc)
            except Exception:
                pass

        ctx.panel.state.near_times_square = near_count
        ctx.panel.state.total_located = len(all_locations)

        lat = [l[1] for l in all_locations] if all_locations else []
        lng = [l[0] for l in all_locations] if all_locations else []

        scatter_data = [
            {
                "lat": lat,
                "lon": lng,
                "mode": "markers",
                "type": "scattermapbox",
                "marker": {
                    "size": 6,
                    "color": "#2563eb",
                    "opacity": 0.7,
                },
            },
            {
                "lat": [40.7580],
                "lon": [-73.9855],
                "mode": "markers",
                "type": "scattermapbox",
                "marker": {
                    "size": 14,
                    "color": "#dc2626",
                    "symbol": "star",
                },
                "name": "Times Square",
            },
        ]
        ctx.panel.data.map_data = scatter_data
        ctx.panel.state.map_layout = {
            "title": "Ubicacion de capturas - NYC",
            "height": 400,
            "mapbox": {
                "style": "open-street-map",
                "center": {"lat": 40.75, "lon": -73.98},
                "zoom": 10,
            },
            "margin": {"l": 0, "r": 0, "t": 40, "b": 0},
        }

    def render(self, ctx):
        panel = types.Object()

        header = types.LazyFieldView(label="FleetControlAI - Supervision de Flota")
        panel.view("header", view=header)

        kvs = types.KeyValueView()
        kvs.add("Capturas con GPS", ctx.panel.state.total_located)
        kvs.add("Cercanas a Times Square (5km)", ctx.panel.state.near_times_square)
        panel.view("loc_stats", view=kvs)

        col = types.Column()
        col.add("header")
        col.add("loc_stats")
        panel.obj("top", view=col)

        map_viz = types.PlotlyView(layout=ctx.panel.state.map_layout)
        panel.obj("map_data", view=map_viz, label="Mapa de flota")

        return types.Property(
            panel,
            view=types.GridView(align_x="center", orientation="vertical"),
        )


def register(p):
    p.register(CopilotoDashboard)
    p.register(CopilotoGeoFence)
    p.register(CopilotoFleetStats)
