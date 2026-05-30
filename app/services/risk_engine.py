PRODUCT_POINTS = {
    "Ambiente": 0,
    "Refrigerado": 2,
    "Congelado": 3,
}

TRANSFER_TIME_POINTS = {
    "Menos de 30 minutos": 0,
    "30 a 60 minutos": 1,
    "1 a 2 horas": 2,
    "Más de 2 horas": 3,
}

EXPOSURE_TIME_POINTS = {
    "Menos de 5 minutos": 0,
    "5 a 15 minutos": 1,
    "15 a 30 minutos": 2,
    "Más de 30 minutos": 3,
}

VEHICLE_STATUS_POINTS = {
    "Listo / adecuado": 0,
    "Pendiente de revisión": 2,
    "No confirmado": 3,
}

LOAD_CONDITION_POINTS = {
    "Cargado inmediatamente": 0,
    "Esperó antes de cargar": 1,
    "Exposición prolongada": 3,
}

BRANCH_STORAGE_POINTS = {
    "Recibido y almacenado inmediatamente": 0,
    "Recibido con espera": 1,
    "No confirmado": 2,
}


def calculate_temperature_risk(shipment: dict) -> dict:
    risk_score = 0
    reasons = []
    recommendations = []
    risk_factors = []

    risk_score += _add_reason(
        reasons,
        risk_factors,
        PRODUCT_POINTS,
        shipment.get("tipo_producto"),
        minimum=2,
        text=lambda value: f"el producto es {value.lower()}",
        factor=lambda value: f"Producto {value.lower()}",
    )
    risk_score += _add_reason(
        reasons,
        risk_factors,
        TRANSFER_TIME_POINTS,
        shipment.get("tiempo_traslado"),
        minimum=2,
        text=lambda value: f"el traslado estimado es {value.lower()}",
        factor=lambda value: f"Traslado de {value.lower()}",
    )
    risk_score += _add_reason(
        reasons,
        risk_factors,
        EXPOSURE_TIME_POINTS,
        shipment.get("tiempo_exposicion"),
        minimum=2,
        text=lambda value: f"la exposición fue de {value.lower()}",
        factor=lambda value: f"Exposición de {value.lower()}",
    )
    risk_score += _add_reason(
        reasons,
        risk_factors,
        VEHICLE_STATUS_POINTS,
        shipment.get("estado_vehiculo"),
        minimum=1,
        text=lambda value: f"el vehículo está en estado: {value.lower()}",
        factor=lambda value: f"Vehículo {value.lower()}",
    )
    risk_score += _add_reason(
        reasons,
        risk_factors,
        LOAD_CONDITION_POINTS,
        shipment.get("condicion_carga"),
        minimum=1,
        text=lambda value: f"la carga tuvo condición: {value.lower()}",
        factor=lambda value: f"Carga: {value.lower()}",
    )
    risk_score += _add_reason(
        reasons,
        risk_factors,
        BRANCH_STORAGE_POINTS,
        shipment.get("almacenamiento_sucursal"),
        minimum=1,
        text=lambda value: f"el almacenamiento en sucursal fue: {value.lower()}",
        factor=lambda value: f"Almacenamiento: {value.lower()}",
    )

    risk_level = classify_risk(risk_score)

    if shipment.get("estado_vehiculo") != "Listo / adecuado":
        recommendations.append("Confirmar condiciones del vehículo antes de salida.")
    if shipment.get("tiempo_exposicion") in ["15 a 30 minutos", "Más de 30 minutos"]:
        recommendations.append("Reducir el tiempo de exposición fuera del almacenamiento adecuado.")
    if shipment.get("almacenamiento_sucursal") != "Recibido y almacenado inmediatamente":
        recommendations.append("Avisar a sucursal para recibir y almacenar el producto al llegar.")
    if risk_level == "Alto":
        recommendations.append("Registrar acción correctiva antes de continuar la entrega.")
    if not recommendations:
        recommendations.append("Mantener procedimiento estándar de traslado.")
    if not risk_factors:
        risk_factors.append("Sin factores críticos registrados.")

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "explanation": build_explanation(risk_level, reasons),
        "recommendations": recommendations,
        "risk_factors": risk_factors,
    }


def classify_risk(score: int) -> str:
    if score <= 3:
        return "Bajo"
    if score <= 6:
        return "Medio"
    return "Alto"


def risk_css_class(level: str) -> str:
    return {
        "Bajo": "risk-low",
        "Medio": "risk-medium",
        "Alto": "risk-high",
    }.get(level, "risk-info")


def build_explanation(level: str, reasons: list[str]) -> str:
    if not reasons:
        return "Riesgo bajo porque las condiciones operativas registradas son adecuadas."

    if len(reasons) == 1:
        reason_text = reasons[0]
    else:
        reason_text = f"{', '.join(reasons[:-1])} y {reasons[-1]}"

    return f"Riesgo {level.lower()} porque {reason_text}."


def _add_reason(
    reasons: list[str],
    risk_factors: list[str],
    table: dict,
    value: str,
    minimum: int,
    text,
    factor,
) -> int:
    points = table.get(value, 0)
    if points >= minimum:
        reasons.append(text(value))
        risk_factors.append(factor(value))
    return points
