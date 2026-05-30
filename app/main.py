from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.data.mock_data import (
    ACTION_OPTIONS,
    BRANCH_STORAGE_OPTIONS,
    CHECKLIST_ITEMS,
    EXPOSURE_TIMES,
    LOAD_CONDITIONS,
    PRODUCT_TYPES,
    TEMPERATURE_RANGES,
    TRANSFER_TIMES,
    VEHICLE_STATUSES,
    build_shipment,
    temperature_range_for,
)
from app.services.risk_engine import calculate_temperature_risk, risk_css_class
from app.services.storage import load_shipments, save_shipments

app = FastAPI(title="Ruta Limpia TempCheck")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

SHIPMENTS = load_shipments()


templates.env.globals["risk_css_class"] = risk_css_class
templates.env.globals["temperature_range_for"] = temperature_range_for


def get_shipment_or_404(shipment_id: int) -> dict:
    for shipment in SHIPMENTS:
        if shipment["id"] == shipment_id:
            return shipment
    raise HTTPException(status_code=404, detail="Entrega no encontrada")


def build_context(request: Request, **extra) -> dict:
    context = {"request": request}
    context.update(extra)
    return context


@app.get("/")
def dashboard(
    request: Request,
    q: str = Query("", alias="q"),
    risk_filter: str = Query("Todos"),
    product_filter: str = Query("Todos"),
):
    enriched_shipments = []
    counts = {"Bajo": 0, "Medio": 0, "Alto": 0}

    for shipment in SHIPMENTS:
        risk = calculate_temperature_risk(shipment)
        counts[risk["risk_level"]] += 1

        if not matches_filters(shipment, risk, q, risk_filter, product_filter):
            continue
        enriched_shipments.append({**shipment, "risk": risk})

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=build_context(
            request,
            shipments=enriched_shipments,
            counts=counts,
            total_count=len(SHIPMENTS),
            q=q,
            risk_filter=risk_filter,
            product_filter=product_filter,
            product_types=PRODUCT_TYPES,
        ),
    )


@app.get("/entregas/nueva")
def new_shipment_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="shipment_form.html",
        context=build_form_context(
            request,
            mode="create",
            title="Agregar entrega",
            action_url="/entregas/nueva",
            shipment=empty_shipment(),
        ),
    )


@app.post("/entregas/nueva")
def create_shipment(
    codigo: str = Form(...),
    producto: str = Form(...),
    tipo_producto: str = Form(...),
    sucursal_destino: str = Form(...),
    conductor: str = Form(...),
    vehiculo: str = Form(...),
    tiempo_traslado: str = Form(...),
    tiempo_exposicion: str = Form(...),
    estado_vehiculo: str = Form(...),
    condicion_carga: str = Form(...),
    almacenamiento_sucursal: str = Form(...),
    observaciones: str = Form(""),
):
    shipment_id = next_shipment_id()
    SHIPMENTS.append(
        build_shipment(
            shipment_id,
            codigo.strip() or f"RL-{shipment_id:03d}",
            producto.strip(),
            tipo_producto,
            sucursal_destino.strip(),
            conductor.strip(),
            vehiculo.strip(),
            tiempo_traslado,
            tiempo_exposicion,
            estado_vehiculo,
            condicion_carga,
            almacenamiento_sucursal,
            observaciones.strip(),
        )
    )
    save_shipments(SHIPMENTS)
    return redirect_to_detail(shipment_id)


@app.get("/entregas/{shipment_id}")
def shipment_detail(request: Request, shipment_id: int):
    shipment = get_shipment_or_404(shipment_id)
    risk = calculate_temperature_risk(shipment)
    return templates.TemplateResponse(
        request=request,
        name="shipment_detail.html",
        context=build_context(
            request,
            shipment=shipment,
            risk=risk,
            checklist_items=CHECKLIST_ITEMS,
            action_options=ACTION_OPTIONS,
        ),
    )


@app.get("/entregas/{shipment_id}/editar")
def edit_shipment_form(request: Request, shipment_id: int):
    shipment = get_shipment_or_404(shipment_id)
    return templates.TemplateResponse(
        request=request,
        name="shipment_form.html",
        context=build_form_context(
            request,
            mode="edit",
            title="Editar entrega",
            action_url=f"/entregas/{shipment_id}/editar",
            shipment=shipment,
        ),
    )


@app.post("/entregas/{shipment_id}/editar")
def edit_shipment(
    shipment_id: int,
    codigo: str = Form(...),
    producto: str = Form(...),
    tipo_producto: str = Form(...),
    sucursal_destino: str = Form(...),
    conductor: str = Form(...),
    vehiculo: str = Form(...),
    tiempo_traslado: str = Form(...),
    tiempo_exposicion: str = Form(...),
    estado_vehiculo: str = Form(...),
    condicion_carga: str = Form(...),
    almacenamiento_sucursal: str = Form(...),
    observaciones: str = Form(""),
):
    shipment = get_shipment_or_404(shipment_id)
    apply_shipment_fields(
        shipment,
        codigo,
        producto,
        tipo_producto,
        sucursal_destino,
        conductor,
        vehiculo,
        tiempo_traslado,
        tiempo_exposicion,
        estado_vehiculo,
        condicion_carga,
        almacenamiento_sucursal,
        observaciones,
    )
    save_shipments(SHIPMENTS)
    return redirect_to_detail(shipment_id)


@app.post("/entregas/{shipment_id}/actualizar-riesgo")
def update_risk_variables(
    shipment_id: int,
    tipo_producto: str = Form(...),
    tiempo_traslado: str = Form(...),
    tiempo_exposicion: str = Form(...),
    estado_vehiculo: str = Form(...),
    condicion_carga: str = Form(...),
    almacenamiento_sucursal: str = Form(...),
    observaciones: str = Form(""),
):
    shipment = get_shipment_or_404(shipment_id)
    shipment.update(
        {
            "tipo_producto": tipo_producto,
            "rango_requerido": temperature_range_for(tipo_producto),
            "tiempo_traslado": tiempo_traslado,
            "tiempo_exposicion": tiempo_exposicion,
            "estado_vehiculo": estado_vehiculo,
            "condicion_carga": condicion_carga,
            "almacenamiento_sucursal": almacenamiento_sucursal,
            "observaciones": observaciones,
        }
    )
    save_shipments(SHIPMENTS)
    return redirect_to_detail(shipment_id)


@app.post("/entregas/{shipment_id}/eliminar")
def delete_shipment(shipment_id: int):
    shipment = get_shipment_or_404(shipment_id)
    SHIPMENTS.remove(shipment)
    save_shipments(SHIPMENTS)
    return RedirectResponse(url="/", status_code=303)


@app.post("/entregas/{shipment_id}/checklist")
async def update_checklist(request: Request, shipment_id: int):
    shipment = get_shipment_or_404(shipment_id)
    form = await request.form()
    shipment["checklist"] = {item: item in form for item in CHECKLIST_ITEMS}
    save_shipments(SHIPMENTS)
    return redirect_to_detail(shipment_id)


@app.post("/entregas/{shipment_id}/acciones")
def add_corrective_action(
    shipment_id: int,
    accion: str = Form(...),
    observacion_accion: str = Form(""),
):
    shipment = get_shipment_or_404(shipment_id)
    label = accion
    if accion == "Otra acción." and observacion_accion.strip():
        label = observacion_accion.strip()
    elif observacion_accion.strip():
        label = f"{accion} Nota: {observacion_accion.strip()}"

    shipment["acciones_correctivas"].append(label)
    save_shipments(SHIPMENTS)
    return redirect_to_detail(shipment_id)


@app.post("/entregas/{shipment_id}/recepcion")
def close_reception(
    shipment_id: int,
    producto_buen_estado: str = Form(...),
    almacenado_inmediatamente: str = Form(...),
    problema_visible: str = Form(...),
    observaciones_recepcion: str = Form(""),
):
    shipment = get_shipment_or_404(shipment_id)
    shipment["recepcion"] = {
        "producto_buen_estado": producto_buen_estado,
        "almacenado_inmediatamente": almacenado_inmediatamente,
        "problema_visible": problema_visible,
        "observaciones": observaciones_recepcion,
        "cerrada": True,
    }
    save_shipments(SHIPMENTS)
    return RedirectResponse(url=f"/entregas/{shipment_id}/resumen", status_code=303)


@app.get("/entregas/{shipment_id}/resumen")
def summary(request: Request, shipment_id: int):
    shipment = get_shipment_or_404(shipment_id)
    risk = calculate_temperature_risk(shipment)
    conclusion = build_conclusion(shipment, risk["risk_level"])
    checklist_done = sum(1 for done in shipment["checklist"].values() if done)

    return templates.TemplateResponse(
        request=request,
        name="summary.html",
        context=build_context(
            request,
            shipment=shipment,
            risk=risk,
            conclusion=conclusion,
            checklist_done=checklist_done,
            checklist_total=len(shipment["checklist"]),
        ),
    )


def build_conclusion(shipment: dict, risk_level: str) -> str:
    reception = shipment["recepcion"]
    has_reception_issue = (
        reception.get("producto_buen_estado") == "No"
        or reception.get("problema_visible") == "Sí"
    )
    has_observations = bool(reception.get("observaciones", "").strip()) or bool(
        shipment.get("observaciones", "").strip()
    )

    if risk_level == "Alto" or has_reception_issue:
        return "Entrega con riesgo alto. Requiere revisión antes de venta."
    if risk_level == "Medio" or has_observations:
        return "Entrega con observaciones. Se recomienda seguimiento."
    return "Entrega controlada."


def redirect_to_detail(shipment_id: int) -> RedirectResponse:
    return RedirectResponse(url=f"/entregas/{shipment_id}", status_code=303)


def matches_filters(
    shipment: dict,
    risk: dict,
    q: str,
    risk_filter: str,
    product_filter: str,
) -> bool:
    normalized_q = q.strip().lower()
    if normalized_q:
        searchable = " ".join(
            [
                shipment.get("codigo", ""),
                shipment.get("producto", ""),
                shipment.get("sucursal_destino", ""),
                shipment.get("conductor", ""),
                shipment.get("vehiculo", ""),
            ]
        ).lower()
        if normalized_q not in searchable:
            return False

    if risk_filter != "Todos" and risk["risk_level"] != risk_filter:
        return False
    if product_filter != "Todos" and shipment["tipo_producto"] != product_filter:
        return False
    return True


def next_shipment_id() -> int:
    if not SHIPMENTS:
        return 1
    return max(shipment["id"] for shipment in SHIPMENTS) + 1


def empty_shipment() -> dict:
    return {
        "codigo": f"RL-{next_shipment_id():03d}",
        "producto": "",
        "tipo_producto": "Ambiente",
        "rango_requerido": temperature_range_for("Ambiente"),
        "sucursal_destino": "",
        "conductor": "",
        "vehiculo": "",
        "tiempo_traslado": "Menos de 30 minutos",
        "tiempo_exposicion": "Menos de 5 minutos",
        "estado_vehiculo": "Listo / adecuado",
        "condicion_carga": "Cargado inmediatamente",
        "almacenamiento_sucursal": "Recibido y almacenado inmediatamente",
        "observaciones": "",
    }


def build_form_context(request: Request, mode: str, title: str, action_url: str, shipment: dict) -> dict:
    return build_context(
        request,
        mode=mode,
        title=title,
        action_url=action_url,
        shipment=shipment,
        product_types=PRODUCT_TYPES,
        temperature_ranges=TEMPERATURE_RANGES,
        transfer_times=TRANSFER_TIMES,
        exposure_times=EXPOSURE_TIMES,
        vehicle_statuses=VEHICLE_STATUSES,
        load_conditions=LOAD_CONDITIONS,
        branch_storage_options=BRANCH_STORAGE_OPTIONS,
    )


def apply_shipment_fields(
    shipment: dict,
    codigo: str,
    producto: str,
    tipo_producto: str,
    sucursal_destino: str,
    conductor: str,
    vehiculo: str,
    tiempo_traslado: str,
    tiempo_exposicion: str,
    estado_vehiculo: str,
    condicion_carga: str,
    almacenamiento_sucursal: str,
    observaciones: str,
) -> None:
    shipment.update(
        {
            "codigo": codigo.strip() or shipment.get("codigo", ""),
            "producto": producto.strip(),
            "tipo_producto": tipo_producto,
            "rango_requerido": temperature_range_for(tipo_producto),
            "sucursal_destino": sucursal_destino.strip(),
            "conductor": conductor.strip(),
            "vehiculo": vehiculo.strip(),
            "tiempo_traslado": tiempo_traslado,
            "tiempo_exposicion": tiempo_exposicion,
            "estado_vehiculo": estado_vehiculo,
            "condicion_carga": condicion_carga,
            "almacenamiento_sucursal": almacenamiento_sucursal,
            "observaciones": observaciones.strip(),
        }
    )
