# Sistema inteligente de priorización de eventos de ciberseguridad

## Fase II - Gestión de Proyectos de Inteligencia Artificial

### Descripción

Este proyecto desarrolla un prototipo académico para clasificar
y priorizar eventos de ciberseguridad mediante aprendizaje automático.

La solución utiliza un modelo de regresión logística entrenado
en Google Colab con datos derivados de CSE-CIC-IDS2018.

El sistema asigna cuatro niveles de prioridad:

- Baja
- Media
- Alta
- Crítica

Las prioridades se basan en una política académica que combina
el tipo de evento con información contextual sintética.

La decisión final corresponde al analista humano.

## Arquitectura

La aplicación integra los siguientes componentes:

1. Frontend desarrollado con HTML, CSS y JavaScript.
2. Backend desarrollado con Python y FastAPI.
3. Modelo de clasificación exportado mediante Joblib.
4. Contenedor Docker para ejecución local.

Flujo de funcionamiento:

Frontend -> FastAPI -> Modelo -> Prioridad sugerida -> Frontend

## Requisitos técnicos

- Docker Desktop o Docker Engine.
- Motor de contenedores Linux.
- Puerto 8001 disponible en el equipo local.
- Acceso a Internet para descargar la imagen base y dependencias.

No es necesario instalar Python localmente para ejecutar
la aplicación mediante Docker.

## Construcción de la imagen

Desde la carpeta raíz del proyecto:

```bash
docker build -t fase-ii-ciberseguridad:1.0 .
```

## Ejecución del contenedor

```bash
docker run -d --name fase-ii-app -p 8001:8000 fase-ii-ciberseguridad:1.0
```

## Acceso a la aplicación

Interfaz web:

http://localhost:8001/

Documentación interactiva de FastAPI:

http://localhost:8001/docs

Verificación del backend:

http://localhost:8001/health

## Endpoints

### GET /health

Comprueba que el backend está disponible.

### POST /predict

Recibe las siguientes variables:

- Label
- Criticidad_Activo
- Exposicion_Internet
- Cuenta_Privilegiada

Ejemplo de solicitud:

```json
{
  "Label": "SSH-Bruteforce",
  "Criticidad_Activo": "Alta",
  "Exposicion_Internet": 1,
  "Cuenta_Privilegiada": 1
}
```

Respuesta esperada:

```json
{
  "prioridad_sugerida": "Crítica",
  "modelo": "Regresión logística",
  "supervision_humana": "requerida"
}
```

## Validación

Se realizaron pruebas funcionales de las cuatro prioridades
y pruebas de validación de entradas incorrectas.

Los escenarios válidos devolvieron HTTP 200.

Las solicitudes con categorías desconocidas o valores fuera
de rango devolvieron HTTP 422.

## Limitaciones

El modelo reproduce una política académica de priorización
basada en etiquetas del dataset y variables contextuales
sintéticas.

Los resultados no representan una validación de efectividad
ante incidentes reales de ciberseguridad.

La supervisión humana se contempla como requisito del sistema,
pero el prototipo actual no registra decisiones del analista.

## Alcance

Prototipo académico desarrollado para demostrar integración
técnica, portabilidad, contenerización y despliegue local.

No está diseñado para operar directamente en un entorno
productivo de ciberseguridad.