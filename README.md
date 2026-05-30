# Ruta Limpia TempCheck

Prototipo MVP web para Muriel construido con FastAPI, Jinja2, HTML, CSS y JavaScript ligero.

## Descripción

Ruta Limpia TempCheck es una aplicación web interna para demostrar cómo Muriel puede controlar el riesgo de temperatura durante el traslado de productos desde fábrica hacia sucursales. El sistema permite revisar entregas activas, evaluar riesgo operativo, completar checklist, registrar acciones correctivas, cerrar recepción y ver un resumen final.

## Problema que resuelve

Durante el traslado, algunos productos pueden perder calidad por exposición prolongada, cadena de frío débil, manipulación, estado del vehículo o falta de coordinación con la sucursal. Este MVP ayuda al personal a documentar y controlar esas condiciones antes y durante la entrega.

## Por qué no usa sensores reales

Muriel actualmente no cuenta con sensores IoT, dataloggers ni máquinas para tomar temperatura automáticamente durante el transporte. Por eso, el prototipo no inventa lecturas reales de temperatura. La solución inicial se enfoca en control operativo digital usando información que el personal sí puede registrar.

## Índice de Riesgo de Temperatura

El riesgo se calcula con un puntaje basado en:

- Tipo de producto: ambiente, refrigerado o congelado.
- Tiempo estimado de traslado.
- Tiempo aproximado de exposición fuera de almacenamiento adecuado.
- Estado del vehículo.
- Condición de carga.
- Almacenamiento en sucursal.

Clasificación:

- 0 a 3 puntos: Riesgo Bajo.
- 4 a 6 puntos: Riesgo Medio.
- 7 o más puntos: Riesgo Alto.

Cada entrega muestra explicación y recomendaciones operativas.

## Correr localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abre:

```text
http://127.0.0.1:8000
```

Si necesitas abrir la app desde otro equipo, contenedor o enlace externo, ejecuta:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Usa `http://`, no `https://`, salvo que tengas un proxy TLS delante.

## Abrir en GitHub Codespaces

1. Sube estos archivos a GitHub.
2. Abre el repositorio en GitHub: `https://github.com/A625A/TemptCheck`
3. Presiona `Code` > `Codespaces` > `Create codespace on main`.
4. Espera a que Codespaces instale las dependencias y arranque la app.
5. Abre el puerto `8000` cuando aparezca la vista previa.

Codespaces usa la configuración de `.devcontainer/devcontainer.json` para instalar `requirements.txt`, ejecutar:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

y abrir la app automáticamente en el puerto `8000`.

## Persistencia de datos

La app guarda entregas, ediciones, checklist, acciones correctivas y cierres de recepción en:

```text
app/data/shipments.json
```

Si el archivo no existe, se crea automáticamente con los datos simulados iniciales.

## Correr con Docker

```bash
docker build -t ruta-limpia-tempcheck .
docker run -p 8000:8000 ruta-limpia-tempcheck
```

Abre:

```text
http://127.0.0.1:8000
```

Para conservar datos aunque elimines el contenedor, monta un volumen:

```bash
docker run -p 8000:8000 -v "$(pwd)/app/data:/app/app/data" ruta-limpia-tempcheck
```

## Limitaciones del MVP

- No mide temperatura real.
- No reemplaza sensores, dataloggers ni controles técnicos.
- Inicia con datos simulados.
- Guarda datos en un archivo JSON local, no en una base de datos real.
- El índice de riesgo es una aproximación para validar la idea.
- Sirve como prototipo para testear con usuarios, no como sistema final.

## Posibles mejoras futuras

- Persistencia en base de datos.
- Roles para fábrica, transporte y sucursal.
- Historial de entregas y reportes.
- Integración futura con sensores o dataloggers si la empresa los adopta.
- Exportación de resúmenes a PDF.
- Validaciones operativas más avanzadas por tipo de producto.
# TemptCheck
