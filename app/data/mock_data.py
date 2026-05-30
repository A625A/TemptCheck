from copy import deepcopy


CHECKLIST_ITEMS = [
    "Producto preparado correctamente.",
    "Producto cargado sin espera prolongada.",
    "Vehículo revisado antes de salida.",
    "Ruta confirmada.",
    "Encargado de sucursal informado.",
    "Producto será almacenado inmediatamente al llegar.",
]

ACTION_OPTIONS = [
    "Reducir tiempo de espera antes de carga.",
    "Confirmar vehículo antes de salida.",
    "Avisar a sucursal para almacenamiento inmediato.",
    "Marcar producto para revisión al llegar.",
    "Reprogramar salida si las condiciones no son adecuadas.",
    "Otra acción.",
]

PRODUCT_TYPES = ["Ambiente", "Refrigerado", "Congelado"]
TEMPERATURE_RANGES = {
    "Ambiente": "15°C a 25°C",
    "Refrigerado": "2°C a 8°C",
    "Congelado": "-18°C o menor",
}
TRANSFER_TIMES = ["Menos de 30 minutos", "30 a 60 minutos", "1 a 2 horas", "Más de 2 horas"]
EXPOSURE_TIMES = ["Menos de 5 minutos", "5 a 15 minutos", "15 a 30 minutos", "Más de 30 minutos"]
VEHICLE_STATUSES = ["Listo / adecuado", "Pendiente de revisión", "No confirmado"]
LOAD_CONDITIONS = ["Cargado inmediatamente", "Esperó antes de cargar", "Exposición prolongada"]
BRANCH_STORAGE_OPTIONS = [
    "Recibido y almacenado inmediatamente",
    "Recibido con espera",
    "No confirmado",
]


def default_checklist() -> dict:
    return {item: False for item in CHECKLIST_ITEMS}


def default_reception() -> dict:
    return {
        "producto_buen_estado": "",
        "almacenado_inmediatamente": "",
        "problema_visible": "",
        "observaciones": "",
        "cerrada": False,
    }


def temperature_range_for(product_type: str) -> str:
    return TEMPERATURE_RANGES.get(product_type, "No definido")


def build_shipment(
    shipment_id: int,
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
    observaciones: str = "",
) -> dict:
    return {
        "id": shipment_id,
        "codigo": codigo,
        "producto": producto,
        "tipo_producto": tipo_producto,
        "rango_requerido": temperature_range_for(tipo_producto),
        "sucursal_destino": sucursal_destino,
        "conductor": conductor,
        "vehiculo": vehiculo,
        "tiempo_traslado": tiempo_traslado,
        "tiempo_exposicion": tiempo_exposicion,
        "estado_vehiculo": estado_vehiculo,
        "condicion_carga": condicion_carga,
        "almacenamiento_sucursal": almacenamiento_sucursal,
        "observaciones": observaciones,
        "checklist": default_checklist(),
        "acciones_correctivas": [],
        "recepcion": default_reception(),
    }


def get_mock_shipments() -> list[dict]:
    shipments = [
        build_shipment(1, "RL-001", "Galletas empacadas", "Ambiente", "Zona 10", "Carlos Méndez", "Unidad 01", "Menos de 30 minutos", "Menos de 5 minutos", "Listo / adecuado", "Cargado inmediatamente", "Recibido y almacenado inmediatamente", "Entrega regular de producto ambiente."),
        build_shipment(2, "RL-002", "Pastel refrigerado", "Refrigerado", "Carretera a El Salvador", "Luis García", "Unidad 04", "30 a 60 minutos", "5 a 15 minutos", "Listo / adecuado", "Esperó antes de cargar", "Recibido con espera", "Validar almacenamiento inmediato en sucursal."),
        build_shipment(3, "RL-003", "Producto congelado", "Congelado", "Oakland", "Mario López", "Unidad 07", "Más de 2 horas", "Más de 30 minutos", "No confirmado", "Exposición prolongada", "No confirmado", "Caso de alto riesgo para demostrar alertas y acciones."),
        build_shipment(4, "RL-004", "Base delicada refrigerada", "Refrigerado", "San Cristóbal", "José Ramírez", "Unidad 03", "1 a 2 horas", "15 a 30 minutos", "Pendiente de revisión", "Esperó antes de cargar", "No confirmado", "Pendiente de revisión previa a salida."),
    ]

    return deepcopy(shipments)
