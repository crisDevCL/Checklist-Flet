import flet as ft
import json
from datetime import date
import os

DB_FILE = "data.json"
TAREAS = [
    "Cuadrar recaudaciones",
    "Actualizar planilla de cierre diario",
    "Cierre de turno en copec fuel",
    "Enviar cuadre de promae",
    "Actualizar planilla de stock Bluemax",
    "Cierre diario de Dinamo",
    "Cierre diario de stock combustibles",
    "Registrar facturas en stock no combustibles",
    "Ingresar pedido de Bluemax granel",
    "Enviar documentos de Bluemax granel recepcionado",
    "Solicitar factura para clientes",
    "Ingresar denuncias por robos declarados",
    "Ingresar llamanos por robos declarados",
    "Enviar respaldos de robos declarados",
    "Enviar AADD pendientes por correo",
    "Cargar documentos fisicos en Google Drive",
    "Cierre semanal de temporis",
    "Actualizacion semanal de precios combustibles"
]

# Cargar datos desde archivo JSON


def cargar_datos():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

# Guardar datos en archivo JSON


def guardar_datos(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main(page: ft.Page):
    page.title = "Checklist Diario"
    page.scroll = ft.ScrollMode.AUTO
    datos = cargar_datos()

    selected_date = date.today().isoformat()
    checkboxes = []
    observaciones = {}

    def guardar_click(e):
        tareas_estado = {t: cb.value for t, cb in zip(TAREAS, checkboxes)}
        obs = {
            t: observaciones[t].value for t in TAREAS if observaciones[t].value}
        datos[selected_date] = {"tareas": tareas_estado, "observaciones": obs}
        guardar_datos(datos)
        page.snack_bar = ft.SnackBar(
            ft.Text("✅ Jornada guardada correctamente"))
        page.snack_bar.open = True
        page.update()

    def cargar_fecha(e):
        nonlocal selected_date
        selected_date = fecha_field.value
        if selected_date in datos:
            entry = datos[selected_date]
            for t, cb in zip(TAREAS, checkboxes):
                cb.value = entry["tareas"].get(t, False)
                observaciones[t].value = entry["observaciones"].get(t, "")
        else:
            for cb in checkboxes:
                cb.value = False
            for obs in observaciones.values():
                obs.value = ""
        page.update()

    fecha_field = ft.TextField(
        label="Fecha (YYYY-MM-DD)", value=selected_date, on_submit=cargar_fecha)
    page.add(fecha_field)

    for tarea in TAREAS:
        cb = ft.Checkbox(label=tarea)
        obs = ft.TextField(label=f"Observación: {tarea}", multiline=True)
        checkboxes.append(cb)
        observaciones[tarea] = obs
        page.add(cb)
        page.add(obs)

    btn_guardar = ft.ElevatedButton("Guardar jornada", on_click=guardar_click)
    page.add(btn_guardar)


ft.app(target=main)
